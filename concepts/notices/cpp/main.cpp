// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/diagnostic.h>
#include <pxr/base/tf/stringUtils.h>
#include <pxr/base/tf/weakBase.h>
#include <pxr/usd/sdf/schema.h>
#include <pxr/usd/usd/common.h>
#include <pxr/usd/usd/notice.h>
#include <pxr/usd/usd/stage.h>


class UpdateNotice : public pxr::TfWeakBase
{
public:
    UpdateNotice(const pxr::UsdStageWeakPtr &stage) {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr(this),
            &UpdateNotice::_callback,
            stage
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::ObjectsChanged &notice,
        const pxr::UsdStageWeakPtr &sender
    ) {
        std::cout << "The triggered sender " << pxr::TfStringify(notice.GetStage()) << '\n';
        std::cout << "Resynced paths [";
        for (auto const &path : notice.GetResyncedPaths())
        {
            std::cout << "%s, ", path.GetText();
        }
        std::cout << "]\n";

        std::cout << "The path Prim that was affected [";
        for (auto const &path : notice.GetChangedInfoOnlyPaths())
        {
            std::cout << "%s, ", path.GetText();
        }
        std::cout << "]\n";

        std::cout << std::boolalpha;
        std::cout
            << "Affected object "
            << notice.AffectedObject(sender->GetPrimAtPath(pxr::SdfPath("/SomeSphere")))
            << '\n';

        std::cout
            << "Resynced? "
            << notice.ResyncedObject(sender->GetPrimAtPath(pxr::SdfPath("/SomeSphere")))
            << '\n';

        std::cout
            << "Changed? "
            << notice.ChangedInfoOnly(sender->GetPrimAtPath(pxr::SdfPath("/SomeSphere")))
            << '\n';
    }
};


class ObjectNoticeGlobal : public pxr::TfWeakBase
{
public:
    ObjectNoticeGlobal() {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr<ObjectNoticeGlobal>(this),
            &ObjectNoticeGlobal::_callback
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::ObjectsChanged &notice
    ) {
        // TODO : How do you print `notice`?
        std::cout << "The triggered stage " << pxr::TfStringify(notice.GetStage()).c_str() << '\n';
    }
};


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
        const pxr::UsdNotice::StageContentsChanged &notice
    ) {
        // TODO : How do you print `notice`?
        std::cout << "The triggered stage " << pxr::TfStringify(notice.GetStage()) << '\n';
    }
};


class StageTargetNoticeGlobal : public pxr::TfWeakBase
{
public:
    StageTargetNoticeGlobal() {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr(this),
            &StageTargetNoticeGlobal::_callback
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::StageEditTargetChanged &notice
    ) {
        // TODO : How do you print `notice`?
        std::cout << "The triggered stage " << pxr::TfStringify(notice.GetStage()) << '\n';
    }
};


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    std::cout << std::boolalpha;

    {
        // XXX : Once `updated` goes out of scope, the listener will stop listening
        UpdateNotice updated {stage};
        stage->DefinePrim(pxr::SdfPath {"/SomeSphere"});
        stage->GetPrimAtPath(pxr::SdfPath {"/SomeSphere"}).SetMetadata(
            pxr::SdfFieldKeys->Comment,
            ""
        );
    }

    stage->DefinePrim(pxr::SdfPath {"/SomeSphere"});
    stage->GetPrimAtPath(pxr::SdfPath {"/SomeSphere"}).SetMetadata(
        pxr::SdfFieldKeys->Comment,
        ""
    );

    // XXX : Unlike Python, which has a `RegisterGlobally` function, C++ re-uses
    // `Register` and uses a separate signature.
    //
    {
        StageContentNoticeGlobal contents;
        ObjectNoticeGlobal objects;
        StageTargetNoticeGlobal targets;

        stage->DefinePrim(pxr::SdfPath {"/Foo"});
        stage->SetEditTarget(stage->GetSessionLayer());
        stage->GetPrimAtPath(pxr::SdfPath {"/Foo"}).SetMetadata(
            pxr::SdfFieldKeys->Comment,
            ""
        );
        stage->GetPrimAtPath(pxr::SdfPath {"/Foo"}).SetMetadata(
            pxr::SdfFieldKeys->Comment,
            "x"
        );
    }

    return 0;
}
