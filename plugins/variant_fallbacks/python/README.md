## How To Run

Because this folder requires a `plugInfo.json` file to be discoverable
by USD, we can't just run the Python file as-is like normal.
Instead, we need to add the directory of `plugInfo.json` to the
`PXR_PLUGINPATH_NAME` environment variable:

```bash
PXR_PLUGINPATH_NAME=`dirname $PWD`/plugin python variant_fallbacks.py
```
