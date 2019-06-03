The USD documentation suggests in a few places (sorry, can't find links
right now) that Prims are meant to have one Payload. This however
doesn't seem to be a requirement.

In the USD glossary, Payloads are described as "a special kind of a
Reference" that is weaker than References. As it turns out, you can
use References and container Prims to collect multiple Payloads into a
single Prim.


### USD
```usda
#usda 1.0

def Xform "SomeTransform" (
    prepend references = [
        </SomeXformCube>,
        </SomeXformSphere>
    ]
)
{
}


def Xform "SomeXformCube" (
    prepend payload = @./cube_payload.usda@</PayloadCubeThing>
)
{
}


def Xform "SomeXformSphere" (
    prepend payload = @./sphere_payload.usda@</PayloadSphereThing>
)
{
}
```

The Python and C++ projects in this concept show how to replicate this, in-code.


# See Also
https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Payload
