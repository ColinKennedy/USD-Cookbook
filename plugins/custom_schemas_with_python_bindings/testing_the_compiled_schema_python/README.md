[custom_schema_include](custom_schema_include.py) shows how to import and use
the custom schemas that were built.

You must build the custom schema class Python bindings before you can
run "custom_schema_include". If you haven't already done this, head over
to [compiling_the_schema](../compiling_the_schema) to get started.


## How To Run
```bash
LD_LIBRARY_PATH=/wherever/you/installed/USD/lib PYTHONPATH=/wherever/you/installed/USD/lib/python:`dirname $PWD`/compiling_the_schema/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/compiling_the_schema/build/install/plugin/usd/testout/resources python custom_schema_include.py

# e.g.
LD_LIBRARY_PATH=/usr/local/USD-19.07/lib PYTHONPATH=/usr/local/USD-19.07/lib/python:`dirname $PWD`/compiling_the_schema/build/install/lib/python2.7/site-packages:$PYTHONPATH PXR_PLUGINPATH_NAME=`dirname $PWD`/compiling_the_schema/build/install/plugin/usd/testout/resources python custom_schema_include.py
```


## Extra Information
The overall project is explained in the folder above this one. Read
through it if you want more of an explanation of what's going on.


## Troubleshooting
If you get an error on-load that looks like this:

```
Traceback (most recent call last):
  File "custom_schema_include.py", line 18, in <module>
    from testout import Testout
  File "/home/selecaoone/repositories/USD-Cookbook/plugins/custom_schemas_with_python_bindings/compiling_the_schema/build/install/
lib/python2.7/site-packages/testout/Testout/__init__.py", line 1, in <module>
    from . import _testout
ImportError: libusd.so: cannot open shared object file: No such file or directory
```

It's because the schema plugin compiled correctly but your current shell
environment doesn't set LD_LIBRARY_PATH correctly. Make sure that you've
set it according to "How To Run" description.
