#!/bin/bash

for comp in gcc-7.2 clang-5.0
do
    for opt in O0 O1 O2 O3 Os
    do
	dir=${comp}-${opt}
	echo "### $dir"
	tmp_dyn=_${dir}_dyn
	tmp_sta=_${dir}_sta
	rm -f ${tmp_dyn} ${tmp_sta}
        echo ${dir}-dynamic_safe
	for dyn in `find ${dir}-dynamic_safe -name '*.gcov'`
	do
	    sta=`echo $dyn | sed -e 's+-dynamic_safe/+-static_safe/+'`
	    cat $dyn >> ${tmp_dyn}
	    cat $sta >> ${tmp_sta}
	done
	./compcov.py ${tmp_sta} ${tmp_dyn} | tee comp_$dir
	rm -f ${tmp_dyn} ${tmp_sta}
    done
done

