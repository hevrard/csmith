#!/usr/bin/env python

import sys
import os

UB_ERRFILE = 'ub_error.txt'
STATIC_SAFE_FILE = 'static_safe.c'
DYN_SAFE_FILE = 'dynamic_safe.c'
TIMEOUT = '30'

def makeAllUnsafe(program):
    source = ''
    with open(program) as f:
        source = f.read()
        source = source.replace('safe_', 'UNSAFE_')
    return source

def collectUB(program, errFile):

    cmd = 'clang-3.8'
    cmd += ' ' + '-fsanitize=undefined'
    cmd += ' ' + '-I${CSMITH_HOME}/runtime'
    cmd += ' ' + program
    cmd += ' > clang_ubsan_out 2> clang_ubsan_err'
    ret = os.system(cmd)
    if ret != 0:
        print('CATCH compiling with UBSan failed')
        print('ERROR: the following command returned non-zero value: {}'.format(ret))
        print(cmd)
        exit(1)
    os.system('rm -f clang_ubsan_out clang_ubsan_err')

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
                # avoid duplicates of columns
                if col not in errorLocation[line]:
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
    return compiler.replace(' ', '') + '_out'

def compileAndRun(compiler):
    os.environ['GCOV_PREFIX_STRIP'] = '4'

    crashed = False

    for program in [STATIC_SAFE_FILE, DYN_SAFE_FILE]:
        token = compiler.replace(' ', '') + '-' + program[:-2]
        os.environ['GCOV_PREFIX'] = '/home/gpu/work/csmith/dynamic-safe/coverage/' + token

        cmd = compiler + ' -I$CSMITH_HOME/runtime ' + program + ' -o a.out'
        cmd += ' > ' + token + '_out 2> ' + token + '_err'
        ret = os.system(cmd)
        if ret != 0:
            print('CATCH compiler crashed')
            print('This command returned {}: {} '.format(ret, cmd))
            crashed = True
        else:
            os.system('rm ' + token + '_out ' + token + '_err')

        cmd = './a.out > ' + outputFromCompiledWith(compiler)
        cmd += ' 2> ' + token + '_exec_err'
        ret = os.system(cmd)

        if ret != 0:
            print('CATCH executable crashed')
            print('This command returned {}: {} '.format(ret, cmd))
            crashed = True
        else:
            os.system('rm ' + token + '_exec_err')

        os.remove('a.out')

    return crashed

######################################################################

seed = sys.argv[1]

#print('Seed: {}'.format(seed))

ret = os.system('csmith --seed {} > {}'.format(seed, STATIC_SAFE_FILE))
if ret != 0:
    print('csmith returns: {}'.format(ret))
    exit(1)

applyUnsafeMath(STATIC_SAFE_FILE)

COMPILERS = [
    # 'clang-5.0',
    # 'gcc-7.2'

    'clang-5.0 -O0',
    'clang-5.0 -O1',
    'clang-5.0 -O2',
    'clang-5.0 -O3',
    'clang-5.0 -Os',
    'gcc-7.2 -O0',
    'gcc-7.2 -O1',
    'gcc-7.2 -O2',
    'gcc-7.2 -O3',
    'gcc-7.2 -Os'
]

crashed = False
for cc in COMPILERS:
    tmpCrashed = compileAndRun(cc)
    crashed = crashed or tmpCrashed

if crashed:
    print('WARNING: due to previous issue, exit now and do not compare outputs')
    exit(1)

ref = ''
for i, cc in enumerate(COMPILERS):
    with open(outputFromCompiledWith(cc)) as f:
        if i == 0:
            ref = f.read()
        else:
            content = f.read()
            if ref != content:
                print('CATCH different output for different compilers')
                exit(1)
print('all compilers lead to same output')
