[custom_schema_include](custom_schema_include.py) shows how to import and use
the custom schemas that were built.

You must build the custom schema class Python bindings before you can
run "custom_schema_include". If you haven't already done this, head over
to [compiling_the_schema](../compiling_the_schema) to get started.


## How To Run
```bash
PYTHONPATH=/wherever/you/installed/USD/lib/python:`dirname $PWD`/compiling_the_schema/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/compiling_the_schema/build/install/plugin/usd/testout/resources python custom_schema_include.py    

# e.g.
PYTHONPATH=/usr/local/USD-19.07/lib/python:`dirname $PWD`/compiling_the_schema/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/compiling_the_schema/build/install/plugin/usd/testout/resources python custom_schema_include.py    
```
