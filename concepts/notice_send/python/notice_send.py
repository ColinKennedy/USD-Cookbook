#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Sdf, Tf, Usd


class testPySender(object):
    pass


class cbClass(object):
    def __init__(self, regType, sendNotice, sender):
        # TODO : ?
        # super(cbClass, self).__init__()

        self.received = 0
        self.regType = regType
        self.sendNotice = sendNotice
        self.sender = sender

    def callback(self, n, s):
        assert n is self.sendNotice
        assert isinstance(self.regType, str) or \
               isinstance(n, self.regType)
        assert s is self.sender
        self.received += 1


def handle_notice(notice, sender):
    print("Handling notice")


def send_custom():
    regNoticeType = Tf.Notice
    sendNotice = Tf.Notice()
    sender = testPySender()
    # notice = Tf.Notice()
    # sender = Sender()
    # callback = Callback(Tf.Notice, notice, sender)
    # Tf.Notice.Register(Tf.Notice, callback.callback, sender)

    cb = cbClass(regNoticeType, sendNotice, sender)
    if (sender):
        l = Tf.Notice.Register(regNoticeType, cb.callback, sender)
    if (sender):
        sendNotice.Send(sender)

    print(cb.received)
    sendNotice.Send(sender)
    print(cb.received)


def send_globally():
    listener = Tf.Notice.RegisterGlobally("TfNotice", handle_notice)
    Tf.Notice().SendGlobally()  # This will print the contents in `handle_notice`
    del listener  # You can also run `listener.Revoke()`
    Tf.Notice().SendGlobally()  # This won't print anything


def main():
    """Run the main execution of the current script."""
    layer = Usd.Stage.CreateInMemory()
    # send_globally()
    send_custom()


if __name__ == "__main__":
    main()
