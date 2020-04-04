This README.md assumes you've read and completed every step in
[the parent directory README file](../README.md).

Everything in this folder is meant to be a "bare minimum" example of
writing Python docstrings, rendering them with Sphinx, and linking
them to the USD documentation. It's a template for your future Python
projects.


## How To Build And View The Documentation

```sh
sphinx-build documentation/source documentation/build
firefox documentation/build/index.html
```


## How It Works
To understand what's going on, you need to know how 2 Sphinx extensions,
[autodoc](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
and
[doxylink](https://sphinxcontrib-doxylink.readthedocs.io/en/stable).

autodoc builds Python documentation as Sphinx HTML pages. Whereas
doxylink is what makes those HTML pages linkable to the USD
documentation.
