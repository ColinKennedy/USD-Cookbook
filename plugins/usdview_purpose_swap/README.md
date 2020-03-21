# Quick Reference
"Purpose Swap" changes between the proxy and render purpose in a single,
convenient button.

When dealing with massive USD stages, switching between purposes can
actually take some time. Even usdview's GUI can be slow so this button
minimizes the menus you must click through to just a single button
press.

![usdview_purpose_swap_demonstration](https://user-images.githubusercontent.com/10103049/77233673-3c41c180-6b66-11ea-85e3-6de9d50e0158.gif)


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
