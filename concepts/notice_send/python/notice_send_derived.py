#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that is a variation of  `notice_send_custom.py`.

This module is used to show how derived Notice classes like
`PyNoticeBase` and `PyNoticeDerived` can be used to send or ignore sent
notices.

"""

# IMPORT STANDARD LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf


class Sender(object):
    """An example class that can be sent with `Tf.Notice`.

    Basically it can be almost anything.

    """

    pass


class Callback(object):
    """A class that keeps track of sender / notice information.

    Important:
        This class is just an example of tracking the registered notice
        / sender. `Tf.Notice.Register` doesn't need an instance of a
        class. It can take a function, instead.

    """

    def __init__(self, registered_type, notice, sender):
        """Keep track of the given information."""
        super(Callback, self).__init__()

        self.counter = 0
        self.registered_type = registered_type
        self.notice = notice
        self.sender = sender

    def callback(self, notice, sender):
        """Print out the notice / sender that triggered this notice.

        In many cases you'd want `notice` and `sender` to be whatever
        was used to register this method. But it doesn't have to be.

        """
        print("Got notice?", notice is self.notice)
        print("Got sender?", sender is self.sender)
        self.counter += 1


class PyNoticeBase(Tf.Notice):
    def func(self):
        return 'func from PyNoticeBase'

class PyNoticeDerived(PyNoticeBase):
    def func(self):
        return 'func from PyNoticeDerived'


def send_custom():
    """Print out notice information when different senders are sent."""
    # XXX : You must define the Notice classes before calling `Regiser`,
    # otherwise USD will error with the message "cannot convert <class
    # '__main__.PyNoticeDerived'> to TfType; has that type been defined
    # as a TfType?"
    #
    Tf.Type.Define(PyNoticeBase)
    Tf.Type.Define(PyNoticeDerived)

    notice = PyNoticeBase()
    sender = Sender()
    callback = Callback(PyNoticeDerived, notice, sender)
    listener = Tf.Notice.Register(PyNoticeDerived, callback.callback, sender)

    sender2 = Sender()
    listener2 = Tf.Notice.Register(PyNoticeDerived, callback.callback, sender2)

    print("Custom count", callback.counter)

    # Note, the sender actually matters here. It has to be whatever was
    # provided to `Tf.Notice.Register`. Otherwise, the `callback` method
    # will never be run.
    #
    # XXX : Because `Register` was given `PyNoticeDerived` object but
    # `notice` is `PyNoticeBase`, sending `sender` and `sender2` will
    # not call `callback`
    #
    notice.Send(sender)
    notice.Send(sender2)

    del listener  # You can also run `listener.Revoke()`
    notice.Send(sender)

    # XXX : This value should still be 0 because `PyNoticeBase` will not
    # trigger functions that were registered to `PyNoticeDerived`.
    #
    print("Custom count", callback.counter)


def main():
    """Run the main execution of the current script."""
    send_custom()


if __name__ == "__main__":
    main()
