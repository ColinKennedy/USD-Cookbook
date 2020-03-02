# Quick Reference

USD's Change Processing sends notifications whenever changes are made.
However, you can make significantly speed up your Sdf calls if you
batch the changes into a single operation, which you can do using
`SdfChangeBlock`.

Because `SdfChangeBlock` is easy to use poorly, check out the
documentation listed in [See Also](#See-Also) before using it in your own
tools.


### C++

```cpp
#include <pxr/usd/sdf/changeBlock.h>

// ...

{
    pxr::SdfChangeBlock batcher;
    // ... do some Sdf API code, here
}
```


### Python

```python
from pxr import Sdf

# ...

with Sdf.ChangeBlock():
    # ... do some Sdf API code, here
```


# See Also
https://graphics.pixar.com/usd/docs/api/class_sdf_change_block.html

https://groups.google.com/d/msg/usd-interest/Bh6_sxij-f8/rnGtLK3tAQAJ
