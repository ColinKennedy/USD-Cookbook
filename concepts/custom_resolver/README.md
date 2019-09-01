This project shows how to create a custom C++ / Python asset resolver,
in USD.

It's the most basic project you can write and does almost nothing. But
it's a good template to build from.


## To build and run
1. Follow the build instructions located in the [C++ project folder](./project).
2. Run this code:

(This code assumes that USD is already sourced and importable)

```python
PXR_PLUGINPATH_NAME=$PWD/project/build/install/resources python run_test/custom_resolver.py
```

If the resolver was built correctly, you should see this output:

```
This should still print an empty string
This should print /bar /bar
```


## See Also
https://graphics.pixar.com/usd/docs/api/class_plug_registry.html#plug_plugInfo

https://github.com/LumaPictures/usd-uri-resolver/tree/master/URIResolver

https://groups.google.com/d/msg/usd-interest/BEHMJAnR3Wo/nhsbEXnoAQAJ

https://groups.google.com/d/msg/usd-interest/rTebJeQQXVA/o09edgGaAgAJ

https://groups.google.com/d/msg/usd-interest/9JrXGGbzBnQ/__u_eV9JBgAJ

https://groups.google.com/d/msg/usd-interest/9JrXGGbzBnQ/_f3oaqBdAwAJ

https://groups.google.com/d/msg/usd-interest/eiSim09c7Bg/DPPzUeatAgAJ
