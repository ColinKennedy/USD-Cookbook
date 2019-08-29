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


## How To Test If It Worked
There are two companion projects next to this project. One tests C++ and
the other tests the Python bindings.

[The C++ Project](../testing_the_compiled_schema_cpp)

[The Python Project](../testing_the_compiled_schema_python)
