#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that shows how to register to Tf.Notice for any kind of object."""

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf
from typing import Any


def main():
    """Run the main execution of the current script."""
    def handle_notice(notice: Tf.Notice, sender: Any):
        print("Handling notice", type(notice), sender)

    listener = Tf.Notice.RegisterGlobally(Tf.Notice, handle_notice)
    Tf.Notice().SendGlobally()  # This will print the contents in `handle_notice`
    del listener  # You can also run `listener.Revoke()`
    Tf.Notice().SendGlobally()  # This won't print anything


if __name__ == "__main__":
    main()
