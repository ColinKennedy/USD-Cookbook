## How To Build

Build this project as you normally would. For example:

```bash
cd build
USD_INSTALL_ROOT=/wherever/you/installed/USD/to cmake ..
make
```


## How To Run

Because this folder requires a `plugInfo.json` file to be discoverable
by USD, we can't just run the Python file as-is like normal.
Instead, we need to add the directory of `plugInfo.json` to the
`PXR_PLUGINPATH_NAME` environment variable:

```bash
cd ..
PXR_PLUGINPATH_NAME=`dirname $PWD`/plugin ./build/run_it
```
