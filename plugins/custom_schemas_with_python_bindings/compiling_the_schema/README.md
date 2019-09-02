## How To Build
This project is built the same way as every other project in this
repository. With a couple minor changes:

```bash
cd build
USD_INSTALL_ROOT=/wherever/you/installed/USD/to cmake ..
make install
```

Note `make` is now `make install` and there's no `./run_it` command.
That's because we're building a library to share with other projects,
not creating an executable program.


## How To Test If It Worked
There are two companion projects which can be used to test if the
schemas were built correctly. One tests C++ and the other tests the
Python bindings.

[The C++ Project](../testing_the_compiled_schema_cpp)

[The Python Project](../testing_the_compiled_schema_python)


## Project Explanation
Most of the files in this project were created by running this command:

```bash
cd src
usdGenSchema .
```

usdGenSchema will create a bunch of files, all of which are completely unaltered.
Some files were created by-hand though. This is the full list:

[module.cpp](src/module.cpp)

[moduleDeps.cpp](src/moduleDeps.cpp)

[`__init__.py`](src/__init__.py)

[`__packageinit__.py`](src/__packageinit__.py)


The latter `.py` files are basically just to make the Python bindings
importable for when we use the schema classes in Python. They're only
"necessary" because of how this project is set up. Technically, they
aren't really needed.

The former files though, [module.cpp](src/module.cpp) and
[moduleDeps.cpp](src/moduleDeps.cpp), are absolutely necessary.


### module.cpp and moduleDeps.cpp
To understand what these files do, open [src/CMakeLists.txt](src/CMakeLists.txt),
remove these lines, and re-build this project

```cmake
add_library(${USDPLUGIN_PYTHON_NAME}
    SHARED
        wrapTokens.cpp
        wrapSimple.cpp
        wrapComplex.cpp
        wrapParamsAPI.cpp
)
```

Once you've done that, you'll probably get an error like this:

```
selecaoone@SelecaoOne:/home/selecaoone/projects/usd_experiments/examples/tricks/custom_schemas_with_python_bindings/compiling_the_schema/build$ PYTHONPATH=/usr/local/USD-19.07/lib/python:$PWD/instal
l/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/install/plugin/usd/testout/resources python ~/temp/schema_test_testout.py
Traceback (most recent call last):
  File "/home/selecaoone////temp/schema_test_testout.py", line 4, in <module>
    from testout import Testout
  File "/home/selecaoone/projects/usd_experiments/examples/tricks/custom_schemas_with_python_bindings/compiling_the_schema/build/install/lib/python2.7/site-packages/testout/Testout/__init__.py", lin
e 1, in <module>
    from . import _testout
ImportError: dynamic module does not define init function (init_testout)
```

This is also why
[every schema class that USD provides also has a module.cpp file](https://github.com/PixarAnimationStudios/USD/search?q=filename%3Amodule.cpp&unscoped_q=filename%3Amodule.cpp)


From what I can see searching online, it looks like when you add dynamic
library to your PYTHONPATH and try to import them in a Python script,
Python expects for that library to have an "entry" init function. USD
does things a bit differently. Instead, "module.cpp" wraps the schema
classes that you generated with `usdGenSchema`, which removes the need
to define an init function yourself. Again, this is just a guess.
Similarly, "moduleDeps.cpp" links USD libraries so that you don't get
any linker errors when "module.cpp" is sourced.

TODO : Check if that's true

**Important**: From a quick test using Python, it looks like this schema
example project doesn't need "moduleDeps.cpp". Only "module.cpp" is
actually required. But it's still good to know about "moduleDeps.cpp",
just in case.


## Troubleshooting Build Issues
Every C++ project in this repository is compiled with GCC 8.3.0 except
for this one. For whatever reason, when compiling with later versions of
GCC, I got exceptions when importing the Python bindings library. The
exact error isn't that important but, for reference, this was the error:

```
Traceback (most recent call last):
  File "/home/selecaoone////temp/schema_test_testout.py", line 4, in <module>
	from testout import Testout
  File "/home/selecaoone/projects/usd_experiments/cpp_test/schema_resolver_hybrid/build/install/lib/python2.7/site-packages/testout/Testout/__init__.py", line 1, in <module>
	from . import _testout
ImportError: /home/selecaoone/projects/usd_experiments/cpp_test/schema_resolver_hybrid/build/install/lib/python2.7/site-packages/testout/Testout/../../../../../plugin/usd/testout.so: undefined symbo
l: _ZN32pxrInternal_v0_19__pxrReserved__6TfType7DeclareERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
```

You may also see similar errors where a USD library fails to link some
STL library, like this if you use a later version of GCC.  For this project, it is highly recommended to use whatever version of GCC USD recommends.
[At time time of writing, this was GCC 4.8](https://github.com/PixarAnimationStudios/USD#dependencies).


# References
[Explanation of the init function error](https://stackoverflow.com/a/24226039/3626104)

[Building and exporting CMake projects](https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right)
