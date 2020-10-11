# Quick Reference
Have you ever been in usdview and wanted to save your current camera
view for later? This quick little plugin does this for you.


# Demonstration
![usdview_copy_camera_demonstration](https://user-images.githubusercontent.com/10103049/95707321-0a7d6e80-0c0e-11eb-9930-acf10ae7dde1.gif)


# How To Run
1. Run this in the terminal

Linux
```sh
echo -e '#usda 1.0\n\ndef Sphere "MyPrim" {\ndouble radius = 4\n}' > some_file.usda
PYTHONPATH=$PWD/plugins:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/plugins/copy_camera:$PXR_PLUGINPATH_NAME usdview some_file.usda
```

2. In the opened usdview, press the "Copy The Current Camera" menu button
3. In the pop-up window, type in the path to where you want this new camera to go.
4. Click "Copy" and you should now have a camera Prim exactly where you current camera is.
