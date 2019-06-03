// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/base/tf/notice.h"


class Callback : public pxr::TfWeakBase {
    public:
        void ProcessNotice(pxr::TfNotice const &) { this->counter += 1; }
        int counter = 0;
};

void ProcessNotice(const pxr::TfNotice&) {}

int main() {
    auto callback = new Callback;
    pxr::TfWeakPtr<Callback> sender {callback};
    auto key = pxr::TfNotice::Register(sender, &Callback::ProcessNotice, sender);

    pxr::TfWeakPtr<Callback> sender2 {callback};
    pxr::TfNotice::Register(sender, &Callback::ProcessNotice, sender2);

    std::cout << "Custom count " << callback->counter << '\n';

    // Note, the sender actually matters here. It has to be whatever was
    // provided to `Tf.Notice.Register`. Otherwise, the `callback` method
    // will never be run.
    //
    pxr::TfNotice().Send(sender);
    pxr::TfNotice().Send(sender2);

    pxr::TfNotice::Revoke(key);
    pxr::TfNotice().Send(sender);

    std::cout << "Custom count " << callback->counter << '\n';

    // pointer clean-up // TODO: replace with unique_ptr?
    delete callback;
    callback = nullptr;

    return 0;
}

    // XXX : Instead of putting `callback` in a scope, you can also run
    // You can also use `pxr::TfNotice::Revoke(key);` (where `key` is
    // the return of `Register`) to force sender to stop listening
