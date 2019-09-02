#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module tests if the custom resolver works."""

# IMPORT FUTURE LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Ar


def main():
    """Run the main execution of the current script."""
    print("This should still print an empty string", Ar.GetResolver().Resolve("this_wont_resolve"))
    print("This should print /bar", Ar.GetResolver().Resolve("/foo"))


if __name__ == "__main__":
    main()
