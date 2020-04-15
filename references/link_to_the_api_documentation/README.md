Ever wanted to build Python documentation which directly linked to USD
documentation but didn't know how?

Turns out, it's pretty easy. There's a some prep work involved, but it isn't much.

Important: **This method of linking to Doxygen requires a Sphinx extension called
sphinxcontrib.doxylink, which requires Python 3. Luckily, USD 20.05+ has
Python 3 support.**


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
identifiers to URLs. Doxygen tag files are like Sphinx's
[objects.inv file](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#showing-all-links-of-an-intersphinx-mapping-file).

Anyway, USD doesn't export tags by default. So you need to install USD
with documentation to generate them.

The basic steps are

- Clone the USD repository
- Enable tag generation in Doxygen
- Build the USD documentation with Doxygen documentation enabled

```sh
git clone https://github.com/PixarAnimationStudios/USD
echo "GENERATE_TAGFILE = api_documentation.tag" >> USD/pxr/usd/usd/Doxyfile.in
python USD/build_scripts/build_usd.py /usr/local/USD --docs
```


## Project Setup
Every step up until this point only has to be done only once. However
this next part relates to how you set up your Sphinx projects.
Everything from this point on has to be done for every Python project.

Luckily though, this isn't that hard either.

In summary:
Check out [example_python_project](example_python_project) to see the final result.
