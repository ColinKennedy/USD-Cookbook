This code is copied from [USD's testUsdValueClips](https://github.com/PixarAnimationStudios/USD/tree/master/pxr/usd/lib/usd/testenv/testUsdValueClips/manifest).


## How to read this section
Open root.usda and read through [this page of USD's documentation](https://graphics.pixar.com/usd/docs/api/_usd__page__value_clips.html). 
That page refers to 2 styles of Value Clips, explicit
metadata and templates. This folder is the explicit metadata.


## Value resolution basics
What is the value of `notInManifestAndInClip` at time 0 if we change
root.usda to this snippet?

```usda
#usda 1.0
(
    startTimeCode = 0
    endTimeCode = 12
)


def "Prim" (
    clips = {
        dictionary default = {
            double2[] active = [(0, 1), (2, 1)]
            asset[] assetPaths = [@./clip_1.usda@, @./clip_2.usda@]
            string primPath = "/Clip"
            double2[] times = [(0, 1), (1, 1), (2, 0), (3, 1)]
        }
    }
    references = @./ref.usda@</Ref>
)
{
}
```

The answer: -10. Here's how we know.

The current stage's time is 0. We look in `active` to see which clip USD
will reference. In this case, the answer is "clip_2.usda" because (0, 1)
means "At 0 time, use the 1st index of `assetPaths`. And the 1st index
of `assetPaths` is clip_2.usda.

How do we read clip_2.usda? Well, open clip_2.usda and follow at
namespace written in `primPath`. In `clip_2.usda`, at `primPath`, there
is a Prim that looks like this:

```usda
def "Clip"
{
    double notInManifestAndInClip.timeSamples = {
        0: 0.0,
        1: -10.0,
    }

    uniform double uniformInManifestAndInClip = 0.0
}
```

In `notInManifestAndInClip`, there's our -10. But that's at time 1. Remember that we're
looking at stage time 0, not 1. So how are we getting -10 at our stage time: 0?
The answer is back in root.usda. Look at the `times` Attribute and it'll be obvious.
`[(0, 1), ...]` means "at stage time: 0, sample the active value clip's time 1".

Basically, `root.usda` `times` Attribute maps "/Clip.notInManifestAndInClip" from time 1 to stage time: 0. And that's how we get to -10.


The question "how do you debug/read value resolution of value clips" works like this:

- For some Attribute + time on the stage:
 - Look at `active` to get the index of the active asset which is read from `assetPaths`
 - Follow `primPath` in that active asset and check the timeSamples on the Attribute
 - Check back at root.usda `times`. The stage time (more often than not)
 is remapped to a timeSample that is different than what you'll find in
 the clip.

Actual Value Clip resolution can be much more complex than
this simple example though. For exmaple: Which clip is
used if `active` doesn't specify a clip for some stage's
time? This question and many others are explained in USD's
documentation so, again, make sure to read 
[this page of USD's documentation](https://graphics.pixar.com/usd/docs/api/_usd__page__value_clips.html)
for further information.

Important:

    The above modified root.usda removed `manifestAssetPath`.
    If you add back in `asset manifestAssetPath = @./clip_manifest.usda@` then
    notInManifestAndInClip will be 3.0 because that Attribute is not in mentioned
    in clip_manifest.usda as a Value Clip Attribute.

    manifestAssetPath is optional. For more information on what it is / why
    mayou y want to use it, see USD's documentation.
