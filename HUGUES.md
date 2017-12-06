Dynamicly Safe Csmith

Notes on using UBSan to relax the safety of math construct in Csmith.

author: Hugues Evrard

# Building GCC with coverage

Call configure with `--enable-coverage`:

    ../gcc-7.2.0/configure -v \
      --prefix=/usr/local/gcc-7.2 \
      --program-suffix=-7.2 \
      --build=x86_64-linux-gnu \
      --host=x86_64-linux-gnu \
      --target=x86_64-linux-gnu \
      --enable-checking=release \
      --enable-languages=c \
      --disable-multilib \
      --enable-coverage


Then (adapt the number of processes to the machine on which you
built):

    make -j 16     # this is for an 8 core CPU

    # The built takes a while

    sudo make install

Then edit `/etc/ld.so.conf` to add:

     /usr/local/gcc-7.2/lib64

And reload:

    sudo ldconfig

Add following to bashrc:

    GCC_720_PATH="/usr/local/gcc-7.2"

    PATH="$GCC_720_PATH/bin:$PATH"
    export PATH

    LD_LIBRARY_PATH="$GCC_720_PATH/lib64:$LD_LIBRARY_PATH"
    export LD_LIBRARY_PATH


# build LLVM with coverage

We consider we build LLVM using gcc. Pass the "--coverage" flag as an
extra C and C++ flag:

    cmake -G "Ninja" \
          -DCMAKE_BUILD_TYPE="Release" \
          -DCMAKE_INSTALL_PREFIX="/usr/local/llvm-5.0" \
          -DLLVM_TARGETS_TO_BUILD="X86" \
          -DLLVM_BUILD_EXAMPLES="OFF" \
          -DLLVM_BUILD_TESTS="OFF" \
          -DLLVM_BUILD_DOCS="OFF" \
          -DCMAKE_C_FLAGS="--coverage" \
          -DCMAKE_CXX_FLAGS="--coverage" \
          /home/gpu/work/llvm-5.0.0.src

Then build, install, and edit bashrc / ldconf in a similar way as with
GCC.

