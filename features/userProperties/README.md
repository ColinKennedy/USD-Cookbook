# Quick Explanation
## Create a userProperty
### C++

```cpp
auto attribute = sphere.GetPrim().CreateAttribute(
    pxr::TfToken {"userProperties:some_attribute"},
    pxr::SdfValueTypeNames->Bool,
    true
);
attribute.Set(false);
```


### Python

```python
attribute = sphere.GetPrim().CreateAttribute(
    "userProperties:some_attribute", Sdf.ValueTypeNames.Bool, True
)
attribute.Set(False)
```


## Find all userProperties
### C++

```cpp
auto is_user_property = [&](std::string const &path) {
    static std::string const properties = "userProperties";

    // If `path` starts with "userProperties" then it's a user property
    return strncmp(path.c_str(), properties.c_str(), strlen(properties.c_str())) == 0;
};

for (auto const &property : sphere.GetPrim().GetAuthoredProperties(is_user_property)) {
    std::cout << property.GetName() << " ";
}
std::cout << '\n';
```


### Python

```python
def is_user_property(node):
    return node.startswith("userProperties:")

print('user properties', sphere.GetPrim().GetAuthoredProperties(is_user_property))
```

# See Also
https://graphics.pixar.com/usd/docs/Maya-USD-Plugins.html
