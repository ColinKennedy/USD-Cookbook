# Quick Reference
"Purpose Swap" changes between the proxy and render purpose in a single,
convenient button.

When dealing with massive USD stages, switching between purposes can
actually take some time. Even usdview's GUI can be slow so this button
minimizes the menus you must click through to just a single button
press.


# How To Run
1. Run this command in the terminal:

```bash
PYTHONPATH=$PWD/plugins:$PYTHONPATH PXR_PLUGINPATH_NAME=$PWD/plugins/purpose_swap:$PXR_PLUGINPATH_NAME usdview $PWD/assets/mesh.usda
```

# Customization
The "Purpose Swap" plugin prefers to use the "proxy" USD purpose
whenever it can. But if you prefer to use another purpose, such as
"guide" or "render", "Purpose Swap" comes with some environment
variables to configure this.

e.g.

This means "prefer the render purpose over the proxy purpose and swap between them."

```bash
export USDVIEW_PURPOSE_SWAP_PRIMARY_PURPOSE=render
export USDVIEW_PURPOSE_SWAP_SECONDARY_PURPOSE=proxy
```

This means "prefer the guide purpose over the render purpose and swap between them."

```bash
export USDVIEW_PURPOSE_SWAP_PRIMARY_PURPOSE=guide
export USDVIEW_PURPOSE_SWAP_SECONDARY_PURPOSE=render
```
