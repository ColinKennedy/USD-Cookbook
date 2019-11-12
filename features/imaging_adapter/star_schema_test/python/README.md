## How To Run
```bash
PYTHONPATH=/wherever/you/installed/USD/lib/python:`dirname $PWD`/star_gprim/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/star_gprim/build/install/plugin/usd//resources python test.py

# e.g.
PYTHONPATH=/usr/local/USD-19.07/lib/python:`dirname $PWD`/star_gprim/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/star_gprim/build/install/plugin/usd/testout/resources python test.py
```
