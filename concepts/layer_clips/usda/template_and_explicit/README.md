This section is copied from [USD's testUsdValueClips folder](https://github.com/PixarAnimationStudios/USD/tree/master/pxr/usd/lib/usd/testenv/testUsdValueClips/clipsets)

If you've read the [explicit folder's README.md](../explicit/README.md)
then this example is an extension of that.

As mentioned before, there are two styles of Value Clip generation.
Explicit and templates. This folder shows off both at once, in `root.usda`.

`Set.non_template_clips` is explicit and `Set.template_clips` shows 
Value Clip template syntax. The main difference of template syntax is how templates are found.

Instead of defining which Value Clip files are acive and for which
time-ranges and each clip's filename, there's a strict naming convention
defined by `templateAssetPath` and files are found starting at
`templateStartTime` time (in this case `./template_clip.00.usda`).
`templateStride` is added to `templateStartTime` over and over again to
find new clip files until `templateEndTime` is reached. Easy, right?
