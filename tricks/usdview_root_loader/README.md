# Quick Reference
"Root Loader" lets you load or unload payloads at the selected Prims or
any of the Prim's children.

## Justification
The "Load" / "Unload" buttons in usdview are too strict. If you have
multiple Prims and even a single one of them doesn't have a payload
assigned to it, the button gets greyed out so you cannot click on it.

This can be very frustrating while opening large sets, because it
requires you to know which Prims have payloads, click exactly those
Prims and only those Prims, and dig through the stage Prim namespace
for every Prim. "Root Loader" addresses these problems without forking
usdview.


# How To Run
1. Run this command in the terminal:

```bash
PYTHONPATH=$PWD/plugins:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/plugins/root_loader:$PXR_PLUGINPATH_NAME usdview $PWD/assets/mesh.usda
```

2. In the opened usdview, select a prim like `</Meshes/Thing>`
3. Go to the "Root Loader" menu and press "Root Unload"
4. Go to the "Root Loader" menu and press "Root Load" to get the selected Prim back
5. You should be able to select parent Prims and load/unload those, too

