#!/usr/bin/env python

import sys

cov1 = sys.argv[1]
cov2 = sys.argv[2]

def getType(line):
    return line.split(':')[0]

def getFilename(line):
    return line.split(':')[1]

def getLineIndexCount(line):
    counter = line.split(':')[1]
    data = counter.split(',')
    assert(len(data) == 2)
    return int(data[0]), int(data[1])

with open(cov1) as f:
    lines1 = f.readlines()

with open(cov2) as f:
    lines2 = f.readlines()

exclu_1 = 0
exclu_2 = 0
both = 0
total = 0

#skipfile = False

for i, l1 in enumerate(lines1):
    l2 = lines2[i]
    t1 = getType(l1)
    t2 = getType(l2)
    assert(t1 == t2)

    # if skipfile and (t1 != 'file'):
    #     continue


    if t1 == 'file':
        fn1 = getFilename(l1)
        fn2 = getFilename(l2)
        assert(fn1 == fn2)

        # print(fn1)
        # if fn1.rsplit()[0].endswith('.h'):
        #     skipfile = True
        #     print('Skip file: ' + fn1)
        # else:
        #     skipfile = False

    elif t1 == 'lcount':
        i1, c1 = getLineIndexCount(l1)
        i2, c2 = getLineIndexCount(l2)
        assert(i1 == i2)
        total += 1
        if (c1 > 0) and (c2 == 0):
            exclu_1 += 1
            #print('{} {}'.format(fn1, i1))
        elif (c1 == 0) and (c2 > 0):
            exclu_2 += 1
            #print('{} {}'.format(fn1, i1))
        elif (c1 > 0) and (c2 > 0):
            both += 1
        else:
            assert((c1 == 0) and (c2 == 0))

    elif t1 == 'function':
        continue

    else:
        print('ERROR: Unknow line type: ' + t1)
        exit(1)


        
percent_both = (float(both) * 100.0) / float(total)
percent_exclu_1 = (float(exclu_1) * 100.0) / float(total)
percent_exclu_2 = (float(exclu_2) * 100.0) / float(total)

print('total:   {:8d}'.format(total))
print('both:    {:8d} ({:6f}%)'.format(both, percent_both))
print('exclu {}: {:8d} ({:6f}%)'.format(cov1, exclu_1, percent_exclu_1))
print('exclu {}: {:8d} ({:6f}%)'.format(cov2, exclu_2, percent_exclu_2))
