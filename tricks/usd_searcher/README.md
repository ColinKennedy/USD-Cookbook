Sometimes, you just have to search a USD file for some text. Most of
the time, if you're looking for something specific, you can just open
up usdview and dig around until you find what you need. But if, for
example, you need to find every relationship containing the phrase "foo"
or "bar", you're in for some trouble.

USD files can refer anywhere on-disk. In studio pipelines, it's very
common for Asset paths to be URIs referring to an off-site location
on-disk or even refer to files in a database.

That's where usd-search comes in. usd-search a command-line utility /
Python module that searches through USD files, recursively.


## Features
- Search through USD Layers, even crate files
- Optionally searches through Asset paths
- Supports regex matching


## How To Use
```bash
PYTHONPATH=$USD_INSTALL_ROOT/lib/python:$PWD/python:$PYTHONPATH ./bin/usd-search foo /some/usd/file.usda
```


## Requirements
- USD must be importable in Python
- (Optional) Your environment should be set up however it needs to be in
order to resolve paths correctly
