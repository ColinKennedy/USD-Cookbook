#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A module that shows how to register to Tf.Notice for specific object(s)."""

# IMPORT STANDARD LIBRARIES
from __future__ import print_function

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Tf, Usd


class Sender(object):
    """An example class that can be sent with `Tf.Notice`.

    Basically it can be almost anything.

    """

    def __init__(self, stage):
        """Store some stage so that it can be retrieved, later."""
        super(Sender, self).__init__()

        self._stage = stage

    def get_stage(self):
        """`pxr.Usd.Stage`: The stored object that was added to this instance."""
        return self._stage


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
        print("Stored stage", sender.get_stage())
        print("Got notice?", notice is self.notice)
        print("Got sender?", sender is self.sender)
        self.counter += 1


def send_custom():
    """Print out notice information when different senders are sent."""
    notice = Tf.Notice()
    some_stage = Usd.Stage.CreateInMemory()
    sender = Sender(some_stage)
    callback = Callback(Tf.Notice, notice, sender)
    listener = Tf.Notice.Register(Tf.Notice, callback.callback, sender)

    sender2 = Sender(some_stage)
    listener2 = Tf.Notice.Register(Tf.Notice, callback.callback, sender2)

    print("Custom count", callback.counter)

    # Note, the sender actually matters here. It has to be whatever was
    # provided to `Tf.Notice.Register`. Otherwise, the `callback` method
    # will never be run.
    #
    notice.Send(sender)
    notice.Send(sender2)

    del listener  # You can also run `listener.Revoke()`
    notice.Send(sender)

    print("Custom count", callback.counter)


def main():
    """Run the main execution of the current script."""
    send_custom()


if __name__ == "__main__":
    main()
