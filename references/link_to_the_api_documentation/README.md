Ever wanted to build Python documentation which directly linked to USD
documentation but didn't know how?

Turns out, it's pretty easy. There's a bit of prep work, but it isn't much.

# USD Documentation Setup
## Installation Setup
### Documentation Tools
For this section, we'll be using [doxylink](https://github.com/sphinx-contrib/doxylink).
Follow the link to its install instructions or just run this:

```sh
pip install sphinxcontrib-doxylink
```

Now install [Sphinx](https://www.sphinx-doc.org/en/1.6/install.html)

```sh
pip install sphinx
```

## USD Documentation
``doxylink`` works by reading a ".tag" file which points Doxygen
identifiers to URLs. Doxygen tag files are like Sphinx's objects.inv file.

Anyway, USD doesn't export tags by default. So you need to install USD
with documentation to generate them.

The basic steps are

- Clone the USD repository
- Enable tags
- Build the USD documentation

```sh
git clone https://github.com/PixarAnimationStudios/USD
echo "GENERATE_TAGFILE = api_documentation.tag" >> USD/pxr/usd/usd/Doxyfile.in
python USD/build_scripts/build_usd.py /usr/local/USD --docs  
```


## Project Setup
Every step up until this point only has to be done once. However this
part is related to setting up your Sphinx projects so that they work
with doxylink. So unfortunately, you need to set this up for each of
your projects.

Luckily though, this isn't that hard either.

In summary:
Check out [example_python_project](example_python_project) to see the final result.
