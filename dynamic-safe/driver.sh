#!/bin/bash

for seed in `seq 4000 4010`
do
    echo "======== START $seed DATE `date`"
    num=`printf "%4.4d" $seed`
    expdir="exp_$num"
    rm -rf $expdir
    mkdir $expdir

    # if test -f $expdir/dynamic_safe.c
    # then
	(
	    cd $expdir
	    ../dynamic-safe.py $seed
	)
    # else
    # 	echo "No dynamic_safe.c found, skip"
    # fi

done
