#!/usr/bin/env python

import sys
import os

program = sys.argv[1]

UB_ERRFILE = 'ub_error.txt'
UB_CFILE = 'ub.c'
TIMEOUT = '30'

def makeAllUnsafe(program):
    source = ''
    with open(program) as f:
        source = f.read()
        source = source.replace('safe_', 'UNSAFE_')
    return source

def collectUB(program, errFile):

    cmd = 'clang'
    cmd += ' ' + '-fsanitize=undefined'
    cmd += ' ' + '-I${CSMITH_HOME}/runtime'
    cmd += ' ' + program
    cmd += ' ' + '> _out 2> _err'
    ret = os.system(cmd)

    if ret != 0:
        print('compilation failed')
        exit(1)

    cmd = 'timeout --kill-after=1 ' + TIMEOUT
    cmd += ' ./a.out > /dev/null 2> ' + errFile
    ret = os.system(cmd)

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

######################################################################

errorLocation = collectUB(program, UB_ERRFILE)
if len(errorLocation) > 0:
    print('Original program has UB!')
    exit(2)

print('Apply UNSAFE everywhere')
with open(UB_CFILE, 'w') as f:
    f.write(makeAllUnsafe(program))

i = 0
while True:
    print('# round {}'.format(i))

    errorLocation = collectUB(UB_CFILE, UB_ERRFILE)

    nbErr = len(errorLocation)
    print('UB errors: {}'.format(nbErr))

    if (nbErr == 0):
        #print('no more UB errors, done')
        break

    #print('Revert the UB to safe math')
    errorLocation = correctErrorLocation(errorLocation)
    nbReverted = revertMacros(UB_CFILE, errorLocation)
    #print('Reverted {} macros'.format(nbReverted))
    if nbReverted == 0:
        print('ERROR: cannot revert any macro, reached a buggy fixpoint?')
        exit(1)
    i += 1
