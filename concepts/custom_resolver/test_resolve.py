#!/usr/bin/env python
# -*- coding: utf-8 -*-


# IMPORT THIRD-PARTY LIBRARIES
from pxr import Ar


def main():
    """Run the main execution of the current script."""
    print('asdffsd', Ar.GetResolver().Resolve("asdf"))


if __name__ == "__main__":
    main()
