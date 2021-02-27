## Quick Explanation
Attributes in USD can have values from multiple sources such as

- time-samples
- linear interpolation (a value between two time-samples)
- default values
- schema fallback values

Because time-sampled Attributes can be offset and scaled when referenced
/ payloaded into another Layer, it can get tough to know how a composed
value was resolved.


### C++
```cpp
bool is_interpolated(pxr::UsdAttribute const &attribute, double frame)
{

    double lower;
    double upper;
    bool has_time_samples;

    attribute.GetBracketingTimeSamples(frame, &lower, &upper, &has_time_samples);

    // XXX : `lower != upper` means "you cannot be interpolating
    // between two values if there is only one value.
    //
    return (has_time_samples && lower != upper && lower != frame);
}
```


### Python
```python
def is_interpolated(attribute, frame):
	"""Check if `attribute` has a "keyframe" at `frame` or if it is interpolated.

	Args:
		attribute (:class:`pxr.Usd.Attribute`):
			Some time-varying USD object to check.
		frame (int or float):
			The specific point in time to check for interpolation.

	Returns:
		bool:
            Return False if `frame` is a "keyframe" or has no
            time-varying values. Otherwise, return True.

	"""
    bracketing = attribute.GetBracketingTimeSamples(frame)

    # Note that some attributes return an empty tuple, some None, from
    # GetBracketingTimeSamples(), but all will be fed into this function.
    #
    return bracketing and (len(bracketing) == 2) and (bracketing[0] != frame)
```


## Resolution Source Enums
A reference for what each USD source enum means

Usd.ResolveInfoSourceFallback: No other value found, so using the schema fallback value (e.g. Sphere.radius fallback is 1.0)
Usd.ResolveInfoSourceDefault: A user-defined default value.
Usd.ResolveInfoSourceValueClips: A value that comes from a value clip
Usd.ResolveInfoSourceTimeSamples: A time-varying value (does not specify interpolation or not)
Usd.ResolveInfoSourceNone: The attribute's value is not defined and no schema fallback exists.


## References
This section's trick was copied
[from usdview](https://github.com/PixarAnimationStudios/USD/blob/d8a405a1344480f859f025c4f97085143efacb53/pxr/usdImaging/usdviewq/common.py#L318-L331)
