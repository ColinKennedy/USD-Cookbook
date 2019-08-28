# Quick Reference

This section is a combination of two different ideas.
- A brilliant [live-coding in usdview post by Brett Levin](https://groups.google.com/d/msg/usd-interest/w3-KivsOuTE/psDcH9p-AgAJ)
- Pixar's [usdview plugins tutorial](https://graphics.pixar.com/usd/docs/Creating-a-Usdview-Plugin.html)

This section is a usdview plugin that can automatically reload the Stage
whenever there are new changes.


# How To Run
1. Use the following commands in the terminal:

Linux
```bash
echo -e '#usda 1.0\n\ndef Sphere "MyPrim" {\ndouble radius = 4\n}' > some_file.usda
PYTHONPATH=$PWD/plugins:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/plugins/auto_reloader:$PXR_PLUGINPATH_NAME usdview some_file.usda
```

2. In the opened usdview, Click "Reloader" > "Toggle Auto-Reload USD
Stage"
3. Open some_file.usda and do anything you'd like. Define new prims,
rename things, change the radius size - anything you want. Without
leaving the text editor, usdview should update with the new changes.
4. To disable the auto-reload feature, click "Reloader" > "Toggle
Auto-Reload USD Stage" again.


# See Also
https://groups.google.com/d/msg/usd-interest/w3-KivsOuTE/psDcH9p-AgAJ

https://graphics.pixar.com/usd/docs/Creating-a-Usdview-Plugin.html
