#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that demonstrates the power of `pxr.Ar.ResolverScopedCache`.

Example:
    This first function run will be slowly because it isn't cached.
    Function "Resolve" was called "10000" times and took "60.3" milliseconds.
    Now run the same function, this time with caching.
    Function "Resolve" was called "10000" times and took "8.1" milliseconds.

"""

# IMPORT STANDARD LIBRARIES
import functools
import time

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Ar


def timeit(function, repeats, name):
    start = time.time()

    for _ in range(repeats):
        function()

    end = time.time()

    print(
        'Function "{name}" was called "{repeats}" times and took "{total:.1f}" milliseconds.'.format(
            name=name, repeats=repeats, total=(end - start) * 1000
        )
    )


def main():
    """Run the main execution of the current script."""
    resolver = Ar.GetResolver()
    function = functools.partial(resolver.Resolve, "foo")

    print("This first function run will be slowly because it isn't cached.")
    timeit(function, 10000, "Resolve without cache")

    print("Now run the same function, this time with caching.")
    with Ar.ResolverScopedCache():
        timeit(function, 10000, "Resolve with cache")


if __name__ == "__main__":
    main()
