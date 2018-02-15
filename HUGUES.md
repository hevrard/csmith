Dynamicly Safe Csmith

Notes on using UBSan to relax the safety of math construct in Csmith.

author: Hugues Evrard, Updates: M. Marcozzi

# Building GCC with coverage

Install required packages using "sudo apt-get install libmpc-dev"
Download gcc-7.2 source and unzip in ../gcc-7.2.0

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

Install required package using "sudo apt install cmake" and "sudo apt install ninja-build"
Download llvm-5.0.0 source and unzip in ../llvm-5.0.0.src
Download clang source and unzip in ../llvm-5.0.0.src/tools/clang
Create a build folder and call cmake from there

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
          ../llvm-5.0.0.src

Then build (using the "ninja" command), install (using the "sudo ninja install" command), and edit bashrc / ldconf  in a similar way as with
GCC.

Add "/usr/local/llvm-5.0/lib" to ldconf. 

Add to bashrc:

    LLVM_500_PATH="/usr/local/llvm-5.0/"

    PATH="$LLVM_500_PATH/bin:$PATH"
    export PATH

    LD_LIBRARY_PATH="$LLVM_500_PATH/lib:$LD_LIBRARY_PATH"
    export LD_LIBRARY_PATH

# Installing CSmith

- Get m4: "sudo apt-get install m4"
- Install CSmith:
cd [csmith-root]
./configure
make
sudo make install
Add to bashrc:
CSMITH_HOME="..." (containing runtime/csmith.h)
export CSMITH_HOME

# Running the tool

- Update the value set for GCOV_PREFIX in dynamic-safe.py (compileAndRun) with the right folder for your machine (do not forget the / at the end) 
- To get ready for having full coverage data, adapt folders in prepare_gcov.sh and generate_gcov.sh, and run prepare_gcov.sh.
- Run driver.sh for program generation (number of programs to generate and seeds can be changed in the script), no undefined behaviour guards removal, compilation with different optim levels of gcc/clang and comparison of run outputs.
- To get full coverage data, run generate_gcov.sh, followed by stat_all.sh.


The `dynamic-safe.py` called by driver.sh take care of setting the `GCOV_PREFIX`
environment variables to generate the coverage data files `.gcda` in
local directories. 

# Some results:

## on 1000 experiments

    gpu@anorien:~/work/csmith/unsafe-math/coverage$ ./compcov.py _gcc_static _gcc_dynamic
    total:     773291
    both:       95715 (12.377617%)           # covered by both static and dynamic
    exclu _gcc_static:      130 (0.016811%)  # exclusive to static
    exclu _gcc_dynamic:     4675 (0.604559%) # exclusive to dynamic

    gpu@anorien:~/work/csmith/unsafe-math/coverage$ ./compcov.py _clang_static _clang_dynamic
    total:    1214300
    both:      109529 (9.019929%)
    exclu _clang_static:      367 (0.030223%)
    exclu _clang_dynamic:     1669 (0.137445%)

## on 10k experiments, 12 december 2017

    gpu@anorien:~/work/csmith/unsafe-math$ awk -f checklog.awk 12_12_2017.txt
    Nb Experiments: 10002
    Timeouts:        3096    
    Max nb round:   17
    Avg nb round:    1.50

    gpu@anorien:~/work/csmith/unsafe-math/coverage$ ./compcov.py _gcc_static _gcc_dynamic
    total:     773291
    both:       95715 (12.377617%)
    exclu _gcc_static:      130 (0.016811%)
    exclu _gcc_dynamic:     4675 (0.604559%)
    
    gpu@anorien:~/work/csmith/unsafe-math/coverage$ ./compcov.py _clang_static _clang_dynamic
    total:    1214300
    both:      109529 (9.019929%)
    exclu _clang_static:      367 (0.030223%)
    exclu _clang_dynamic:     1669 (0.137445%)

## on approx. 2k experiments, with different optimisation flags, 14 december

    ### gcc-7.2-O0
    total:     773291
    both:       95674 (12.372315%)
    exclu _gcc-7.2-O0_sta:      123 (0.015906%)
    exclu _gcc-7.2-O0_dyn:     4528 (0.585549%)

    ### gcc-7.2-O1
    total:     773291
    both:      181996 (23.535254%)
    exclu _gcc-7.2-O1_sta:     2368 (0.306224%)
    exclu _gcc-7.2-O1_dyn:     4544 (0.587618%)

    ### gcc-7.2-O2
    total:     773291
    both:      213817 (27.650264%)
    exclu _gcc-7.2-O2_sta:     2016 (0.260704%)
    exclu _gcc-7.2-O2_dyn:     3737 (0.483259%)

    ### gcc-7.2-O3
    total:     773291
    both:      232117 (30.016772%)
    exclu _gcc-7.2-O3_sta:     1973 (0.255143%)
    exclu _gcc-7.2-O3_dyn:     3981 (0.514813%)

    ### gcc-7.2-Os
    total:     773291
    both:      209563 (27.100147%)
    exclu _gcc-7.2-Os_sta:     2145 (0.277386%)
    exclu _gcc-7.2-Os_dyn:     3876 (0.501234%)

    ### clang-5.0-O0
    total:    1214300
    both:      109781 (9.040682%)
    exclu _clang-5.0-O0_sta:      209 (0.017212%)
    exclu _clang-5.0-O0_dyn:     1878 (0.154657%)

    ### clang-5.0-O1
    total:    1214300
    both:      203964 (16.796838%)
    exclu _clang-5.0-O1_sta:     2023 (0.166598%)
    exclu _clang-5.0-O1_dyn:     2968 (0.244421%)

    ### clang-5.0-O2
    total:    1214300
    both:      219996 (18.117105%)
    exclu _clang-5.0-O2_sta:     1297 (0.106811%)
    exclu _clang-5.0-O2_dyn:     1720 (0.141645%)

    ### clang-5.0-O3
    total:    1214300
    both:      221813 (18.266738%)
    exclu _clang-5.0-O3_sta:     1578 (0.129951%)
    exclu _clang-5.0-O3_dyn:     1677 (0.138104%)

    ### clang-5.0-Os
    total:    1214300
    both:      214957 (17.702133%)
    exclu _clang-5.0-Os_sta:     1297 (0.106811%)
    exclu _clang-5.0-Os_dyn:     1768 (0.145598%)

