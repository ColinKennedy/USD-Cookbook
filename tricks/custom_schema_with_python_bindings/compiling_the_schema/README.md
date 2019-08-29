## How To Build
This project is built the same way as every other project in this
repository. With a couple minor changes:

```bash
cd build
USD_INSTALL_ROOT=/wherever/you/installed/USD/to cmake ..
make install
```

Note `make` is now `make install` and there's no `./run_it` command
because we aren't making an executable in this project.

# TODO : Explain module.cpp and moduleDeps.cpp

## How To Test If It Worked
There are two companion projects which can be used to test if the
schemas were built correctly. One tests C++ and the other tests the
Python bindings.

[The C++ Project](../testing_the_compiled_schema_cpp)

[The Python Project](../testing_the_compiled_schema_python)


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
