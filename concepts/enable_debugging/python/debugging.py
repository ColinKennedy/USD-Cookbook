#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test out how to enable debug messages in USD."""

# IMPORT STANDARD LIBRARIES
import sys

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf, Usd

# XXX : You can optionally redirec debug output to a custom file
Tf.Debug.SetOutputFile(sys.__stdout__)


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()

    # XXX : The actual symbols are defined in C++ across many files.
    # You can query them using `Tf.Debug.GetDebugSymbolNames()` or by
    # searching for files that call the `TF_DEBUG_CODES` macro in C++.
    # (Usually this is in files named "debugCodes.h").
    #
    symbols = Tf.Debug.GetDebugSymbolNames()

    # XXX : Check if debug symbols are enabled
    # (on my machine, they're all False by default)
    #
    for symbol in symbols:
        print(Tf.Debug.IsDebugSymbolNameEnabled(symbol))

    # XXX : Here's a full description of everything
    print("Descriptions start")
    print(Tf.Debug.GetDebugSymbolDescriptions())
    print("Descriptions end")

    # XXX : Enable change processing so we can see something happening
    # You can also use glob matching. Like "USD_*" to enable many flags
    # at once.
    #
    Tf.Debug.SetDebugSymbolsByName("USD_CHANGES", True)
    stage.DefinePrim("/SomePrim")  # This line will print multiple messages to stdout


if __name__ == "__main__":
    main()
