## Explanation

The `specializes` Composition Arc is a bit weird. The USD glossary does
a decent job of explaining how it works but I was hoping to put it in
simpler terms. Both for my understanding and others.

It may be an over-simplification but `specializes` is a way of
preventing and "protecting" changes that are made to a specialized Prim.

This folder shows a scenario where `specializes` is used to prevent
edits from other, stronger layers.

There's 3 layers:

- settings.usda
- modelling.usda
- layout.usda

settings.usda has some camera settings that layout.usda is expected to
use. They do this by referencing the camera and changing its settings,
directly. The layout.usda layer also brings in modelling.usda so that it
can reference a model and place it into their scene.

The problem is, a modeller makes a mistake and authors an opinion onto
the cameras in settings.usda. If you look at the code in layout.usda and
then open it as a stage, you'll see the results of this change.

The </_class_CameraSettings> class gets overridden by
modelling and its value make it into the final USD stage. The
</_class_CameraSettingsSpecialized> class is also overridden by
modelling but the value that modelling authored doesn't make it onto
the final USD stage. Why? Because </_class_CameraSettingsSpecialized>
is specialized and its authored `focalLength` property is defined in
the specialized Prim. So the value for `focalLength` that was authored
in settings.usda makes it all the way into layout.usda even though the
modelling.usda Layer tried to override `focalLength` in between.

If the same situation happened and </_class_CameraSettingsSpecialized>
used `inherits` instead of `specializes`, the value for `focalLength`
would have been overridden in modelling.usda.


## Final Note
Asute users of USD will point out that the above scenario can also be solved even if </_class_CameraSettingsSpecialized> used `inherits` if you include `@./settings.usda` in the `subLayers` of layout.usda like so:

```usda
(
    subLayers = [
        @./settings.usda@,
        @./modelling.usda@,
    ]
)
```

This also works and should probably be preferred whenever possible. That
said, just consider the `specializes` solution when there's no other
option.
