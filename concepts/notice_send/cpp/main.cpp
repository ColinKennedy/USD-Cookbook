// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/base/tf/weakBase.h"
#include "pxr/usd/sdf/notice.h"
#include "pxr/usd/usd/notice.h"
#include "pxr/usd/usd/stage.h"


class StageContentNoticeGlobal : public pxr::TfWeakBase
{
public:
    StageContentNoticeGlobal() {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr(this),
            &StageContentNoticeGlobal::_callback
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::StageNotice &notice
    ) {
        // TODO : How do you print `notice`?
        printf("The triggered stage %s\n", pxr::TfStringify(notice.GetStage()).c_str());
    }
};


int main() {
    auto layer = pxr::SdfLayer::CreateAnonymous();
    auto handle = layer->Find("foo");

    StageContentNoticeGlobal contents;
    pxr::SdfNotice::LayerDidReplaceContent().Send(handle);

    return 0;
}
