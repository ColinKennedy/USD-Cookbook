## How to build / install
```
cd build
sudo USD_INSTALL_ROOT=/usr/local/USD-19.07 cmake3 ..
sudo make install
PYTHONPATH=/usr/local/USD-19.07/lib/python:$PWD/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/install/plugin/usd/testout/resources python ~/temp/schema_test_testout.py
```
