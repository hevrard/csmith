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

