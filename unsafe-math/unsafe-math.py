#!/usr/bin/env python

import sys
import os

UB_ERRFILE = 'ub_error.txt'
DYN_SAFE_FILE = 'dyn_safe.c'
TIMEOUT = '30'

def makeAllUnsafe(program):
    source = ''
    with open(program) as f:
        source = f.read()
        source = source.replace('safe_', 'UNSAFE_')
    return source

def runCmd(cmd):
    cmd += ' > _out 2> _err'
    ret = os.system(cmd)
    if ret != 0:
        print('ERROR: the following command returned non-zero value: {}'.format(ret))
        print(cmd)
        exit(1)
    os.system('rm -f _out _err')

def collectUB(program, errFile):

    cmd = 'clang-3.8'
    cmd += ' ' + '-fsanitize=undefined'
    cmd += ' ' + '-I${CSMITH_HOME}/runtime'
    cmd += ' ' + program
    runCmd(cmd)
        
    cmd = 'timeout --kill-after=1 ' + TIMEOUT
    cmd += ' ./a.out > /dev/null 2> ' + errFile
    ret = os.system(cmd)

    os.remove('a.out')
    
    if ret != 0:
        print('timeout')
        exit(124)

    # dictionnary: line -> list of columns
    errorLocation = {}
    with open(errFile) as f:
        for errLine in f:
            if errLine.startswith(program):
                print('UB_ERR: ' + errLine)
                location = errLine.split(':')[1:3]
                line = int(location[0])
                col = int(location[1])
                if line not in errorLocation:
                    errorLocation[line] = []
                errorLocation[line].append(col)
    return errorLocation

def correctErrorLocation(errorLocation):
    # Correct the offset of one between lines and columns reported by
    # UBsan, and their index in string arrays obtained in python.
    corrected = {}
    for line, cols in errorLocation.iteritems():
        corrected[line - 1] = map(lambda x : x - 1 , cols)
    return corrected

def revertMacros(program, errorLocation):
    with open(program) as f:
        progLines = f.readlines()

    nbReverted = 0
    for lineIndex, cols in errorLocation.iteritems():
        line = progLines[lineIndex]
        safeLine = ''

        prev = 0

        for col in cols:

            if line.startswith('UNSAFE_', col):
                safeLine += line[prev:col] + 'safe'
                prev = col + len('UNSAFE')
                nbReverted += 1
            else:
                print('SKIP error at: {} {}'.format(lineIndex, col))

        safeLine += line[prev:]
        progLines[lineIndex] = safeLine
    with open(program, 'w') as f:
        for line in progLines:
            f.write(line)
    return nbReverted

def applyUnsafeMath(program):
    errorLocation = collectUB(program, UB_ERRFILE)
    if len(errorLocation) > 0:
        print('Original program has UB!')
        exit(2)

    print('Apply UNSAFE everywhere')
    with open(DYN_SAFE_FILE, 'w') as f:
        f.write(makeAllUnsafe(program))

    i = 0
    while True:
        print('# round {}'.format(i))

        errorLocation = collectUB(DYN_SAFE_FILE, UB_ERRFILE)

        nbErr = len(errorLocation)
        print('UB errors: {}'.format(nbErr))

        if (nbErr == 0):
            #print('no more UB errors, done')
            break

        #print('Revert the UB to safe math')
        errorLocation = correctErrorLocation(errorLocation)
        nbReverted = revertMacros(DYN_SAFE_FILE, errorLocation)
        #print('Reverted {} macros'.format(nbReverted))
        if nbReverted == 0:
            print('ERROR: cannot revert any macro, reached a buggy fixpoint?')
            exit(1)
        i += 1

def outputFromCompiledWith(compiler):
    return compiler.replace(' -', '_') + '_out'
        
def compileAndRun(program, compiler):
    cmd = compiler + ' -I$CSMITH_HOME/runtime ' + program + ' -o a.out'
    runCmd(cmd)

    cmd = './a.out > ' + outputFromCompiledWith(compiler)
    ret = os.system(cmd)

    if ret != 0:
        print('This command returned {}: {} '.format(ret, cmd))
        exit(1)

    os.remove('a.out')
        
######################################################################

seed = sys.argv[1]

#print('Seed: {}'.format(seed))

ret = os.system('csmith --seed {} > test.c'.format(seed))
if ret != 0:
    print('csmith returns: {}'.format(ret))
    exit(1)

applyUnsafeMath('test.c')

COMPILERS = [
    'clang -O0',
    'clang -O1',
    'clang -O2',
    'clang -O3',
    'clang -Os',
    'gcc -O0',
    'gcc -O1',
    'gcc -O2',
    'gcc -O3',
    'gcc -Os'
]

for cc in COMPILERS:
    compileAndRun(DYN_SAFE_FILE, cc)

ref = ''
for i, cc in enumerate(COMPILERS):
    with open(outputFromCompiledWith(cc)) as f:
        if i == 0:
            ref = f.read()
        else:
            content = f.read()
            if ref != content:
                print('different output for different compilers')
print('all compilers lead to same output')
