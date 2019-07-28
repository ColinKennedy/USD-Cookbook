# How To Run
This C++ project requires a `plugInfo.json` to be visible to USD so we
can't simply call `./run_it` like usual. In a pipeline, your environment
would already be set up to already include any environment variables you
need but for our simple project, this is all you have to do to run it:


```bash
PXR_PLUGINPATH_NAME=`dirname $PWD`/definition python plugin_metadata.py
```

If the `plugInfo.json` parent directory is not found in `PXR_PLUGINPATH_NAME`, you will get this error message:

```
Traceback (most recent call last):
  File "plugin_metadata.py", line 26, in <module>
    main()
  File "plugin_metadata.py", line 18, in main
    ), message
AssertionError: Plugin Metadata was not sourced correctly
```
