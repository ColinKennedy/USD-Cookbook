## Quick Explanation
In USD's Sdf API, you can set time sample values. But the function call
isn't very obvious. Normally if you were setting time-codes / values
on an Attribute, you'd expect to be able to do that from the Attribute
itself. But in Sdf API, you set the time-code / value pair not from the
SdfAttributeSpec / UsdAttribute but from its parent SdfLayer.

### C++
```cpp
layer->SetTimeSample(
    attribute->GetPath(),
    10.5  /* time code */,
    9,  /* value */
);
```


### Python
```python
layer = stage.GetEditTarget().GetLayer()  # By default, this is `stage.GetRootLayer`
time_code = 10.5
value = 9  # An arbitrary value
layer.SetTimeSample(attribute.GetPath(), time_code, value)
```


## See Also
[SetTimeSample](https://graphics.pixar.com/usd/docs/api/class_sdf_layer.html)
