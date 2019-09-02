#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""DCC-agnostic functions that are generally useful."""

STEP = 1.0


def frange(start, stop=None, step=STEP):
    """Create a range of values like Python's built-in "range" function.

    This function will include `start` in its return results but
    excludes `stop`. Just like the way that Python's built-in "range"
    function does.

    Reference:
        https://pynative.com/python-range-for-float-numbers/

    Args:
        start (float or int):
            The value that will start the range.
        stop (float or int or NoneType, optional):
            The value that is used to stop iterating. If no value is
            given then this range will start at 0 and go until it
            reaches the `start` value.
        step (float or int, optional):
            The rate that `start` advances to `stop`. Default: 1.0.

    Yields:
        float or int: The start range + every value

    """
    # Use float number in range() function
    # if stop and step argument is null set start=0.0 and step = 1.0
    if stop is None:
        stop = start
        start = 0.0

    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break

        yield start

        start += step
