# Quick Reference
"Root Loader" lets you load or unload payloads at the selected Prims or
any of the Prim's children.


# How To Run
1. Run this command in the terminal:

```bash
PYTHONPATH=$PWD/plugins:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/plugins/root_loader:$PXR_PLUGINPATH_NAME usdview $PWD/assets/mesh.usda
```

2. In the opened usdview, select a prim like `</Meshes/Thing>`
3. Go to the "Root Loader" menu and press "Root Unload"
4. Go to the "Root Loader" menu and press "Root Load" to get the selected Prim back
5. You should be able to select parent Prims and load/unload those, too


# Justification
usdview already comes with "Load" / "Unload" buttons, but they are too
strict. If you have multiple Prims selected, every single Prim in the
selection has to have a payload underneath it. Otherwise, the "Load" /
"Unload" buttons get greyed out. Now imagine you have a set with 300
payloads, they're each nested within other Prims, and you now have to
expand the QTreeWidget in usdview, find exactly the Prims you're looking
for, manually select each one, and then select "Unload".

"Root Loader" lets you just select a single ancester Prim and every Prim
underneath it will be unloaded. All without forking usdview or changing
the way usdview works.


