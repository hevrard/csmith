output_dir=/home/osboxes/csmith/dynamic-safe/coverage/

cd $output_dir

cd clang-5.0-O0-dynamic_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O0-static_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O1-dynamic_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O1-static_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O2-dynamic_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O2-static_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O3-dynamic_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-O3-static_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-Os-dynamic_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../clang-5.0-Os-static_safe
for no in `find . -name '*.gcno'`
do
    rel_path=${no%/*}
    file_name_extension=${no##*/}
    file_name=${file_name_extension%.cpp.gcno}
    mv $rel_path"/"$file_name".cpp.gcno" $rel_path"/"$file_name".gcno"
    mv $rel_path"/"$file_name".cpp.gcda" $rel_path"/"$file_name".gcda"
    mv $rel_path"/../../"$file_name".cpp" $rel_path"/"$file_name".cpp"
done
for no in `find . -name '*.cpp'`
do
    gcov -i $no
done

cd ../gcc-7.2-O0-dynamic_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O0-static_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O1-dynamic_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O1-static_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O2-dynamic_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O2-static_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O3-dynamic_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-O3-static_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-Os-dynamic_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done

cd ../gcc-7.2-Os-static_safe
for no in `find . -name '*.c'`
do
    gcov -i $no
done



