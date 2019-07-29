# How To Build
Build this project as normal:

```bash
cd build
USD_INSTALL_ROOT=/wherever/you/installed/USD/to cmake ..
make
```

# How To Run
This C++ project requires a `plugInfo.json` to be visible to USD so we
can't simply call `./run_it` like usual. In a pipeline, your environment
would already be set up to already include any environment variables you
need but for our simple project, this is all you have to do to run it:


```bash
cd ..
PXR_PLUGINPATH_NAME=`dirname $PWD`/definition ./build/run_it
```

If the `plugInfo.json` parent directory is not found in `PXR_PLUGINPATH_NAME`, you will get this error message:

```
run_it: $PWD/main.cpp:17: int main(): Assertion `fallback == 12.0 && "Plugin Metadata was not sourced correctly"' failed.
```
