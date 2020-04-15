This README.md assumes you've read and completed every step in
[the parent directory README file](../README.md).

Everything in this folder is meant to be a "bare minimum" example of
writing Python docstrings, rendering them with Sphinx, and linking
them to the USD documentation. It's a template for your future Python
projects.


## How To Build And View The Documentation
- Make sure your Python modules are importable (if you plan to have Python docstrings rendered by Sphinx)
- point USD_INSTALL_ROOT to your root USD install location

```sh
mkdir documentation/build
PYTHONPATH=$PWD/python:$PYTHONPATH USD_INSTALL_ROOT=/usr/local/USD sphinx-build documentation/source documentation/build
firefox documentation/build/index.html
```

### Extra Install Requirements
The [example_file.py module](python/example_file.py) shows how to
document with 2 different documentation styles: Sphinx's built-in style and Google Style.

Google Style Python docstrings require the
[Napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).

Since many people write with this style, it's included in this example.
But it's not required.


## How It Works
Docstrings in Python are rendered by Sphinx using the
[autodoc extension](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
and linking between Python and the Doxygen documentation is handled by the
[doxylink extension](https://sphinxcontrib-doxylink.readthedocs.io/en/stable).
