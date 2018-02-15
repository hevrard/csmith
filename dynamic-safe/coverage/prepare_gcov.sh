llvm_source=/home/osboxes/llvm-5.0.0.src/
llvm_build=/home/osboxes/llvm-5.0.0.bld/
gcc_source=/home/osboxes/gcc-7.2.0/
output_dir=/home/osboxes/csmith/dynamic-safe/coverage/

cd $output_dir
rm -rf cover
mkdir cover
cd cover
mkdir clang
cp -r $llvm_source/lib/* .
cp -r $llvm_source/tools/clang/lib ./clang/
cp -r $llvm_source/tools/clang/tools ./clang/
cp -r $llvm_build/lib/* .
cp -r $llvm_build/tools/clang/lib ./clang/
cp -r $llvm_build/tools/clang/tools ./clang/
cd ..
rm -rf clang-5.0-O0-dynamic_safe
rm -rf clang-5.0-O0-static_safe
rm -rf clang-5.0-O1-dynamic_safe
rm -rf clang-5.0-O1-static_safe
rm -rf clang-5.0-O2-dynamic_safe
rm -rf clang-5.0-O2-static_safe
rm -rf clang-5.0-O3-dynamic_safe
rm -rf clang-5.0-O3-static_safe
rm -rf clang-5.0-Os-dynamic_safe
rm -rf clang-5.0-Os-static_safe
cp -r cover clang-5.0-O0-dynamic_safe
cp -r cover clang-5.0-O0-static_safe
cp -r cover clang-5.0-O1-dynamic_safe
cp -r cover clang-5.0-O1-static_safe
cp -r cover clang-5.0-O2-dynamic_safe
cp -r cover clang-5.0-O2-static_safe
cp -r cover clang-5.0-O3-dynamic_safe
cp -r cover clang-5.0-O3-static_safe
cp -r cover clang-5.0-Os-dynamic_safe
cp -r cover clang-5.0-Os-static_safe

cd $output_dir
rm -rf cover
mkdir cover
cd cover
mkdir gcc
cp -r $gcc_source/gcc .
cp -r $gcc_source/host-x86_64-linux-gnu/gcc .
cd ..
rm -rf gcc-7.2-O0-dynamic_safe
rm -rf gcc-7.2-O0-static_safe
rm -rf gcc-7.2-O1-dynamic_safe
rm -rf gcc-7.2-O1-static_safe
rm -rf gcc-7.2-O2-dynamic_safe
rm -rf gcc-7.2-O2-static_safe
rm -rf gcc-7.2-O3-dynamic_safe
rm -rf gcc-7.2-O3-static_safe
rm -rf gcc-7.2-Os-dynamic_safe
rm -rf gcc-7.2-Os-static_safe
cp -r cover gcc-7.2-O0-dynamic_safe
cp -r cover gcc-7.2-O0-static_safe
cp -r cover gcc-7.2-O1-dynamic_safe
cp -r cover gcc-7.2-O1-static_safe
cp -r cover gcc-7.2-O2-dynamic_safe
cp -r cover gcc-7.2-O2-static_safe
cp -r cover gcc-7.2-O3-dynamic_safe
cp -r cover gcc-7.2-O3-static_safe
cp -r cover gcc-7.2-Os-dynamic_safe
cp -r cover gcc-7.2-Os-static_safe

rm -rf cover




