// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/base/tf/notice.h"


class MainListener : public pxr::TfWeakBase {
public:
    MainListener() {
        // Register for invokation in any thread
        pxr::TfWeakPtr<MainListener> me(this);
        pxr::TfNotice::Register(me, &MainListener::some_function);
    }

    void some_function(pxr::TfNotice const &notice) {
        // XXX : If you're working in a threaded
        // environment, you need to lock this method. See
        // "USD/pxr/base/lib/tf/testenv/notice.cpp" for details.
        //
        std::cout << "Handle notice\n";
    }
};


int main() {
    {
        MainListener listener;
        pxr::TfNotice().Send();  // This will print the contents in `handle_notice`
    }
    // XXX : Instead of putting `listener` in a scope, you can also run
    // `listener.Revoke()`

    pxr::TfNotice().Send();  // This won't print anything

    return 0;
}
