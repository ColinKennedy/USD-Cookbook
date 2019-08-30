You must build the custom schema classes used in this project before you
can follow the build steps below. If you haven't already done this, head
over to [compiling_the_schema](../compiling_the_schema) to get started.


## How To Build
Use the same build + compile steps as any other project in this repository.

In other words, this:
```bash
cd ./build
USD_INSTALL_ROOT=/wherever/you/installed/USD cmake3 ..
# USD_INSTALL_ROOT=/usr/local/USD-19.07 cmake3 ..
make
./run_it
```

### Important Build Note
If you have any problems building and compiling this project, Make sure that
the GCC version that you're using to run `make` with matches the GCC version
that was used build the custom schemas.

`gcc --version`  <-- Check the version

`which gcc`  <-- Check the path on-disk, if needed


## Extra Information
The overall project is explained in the folder above this one. Read
through it if you want more of an explanation of what's going on.
