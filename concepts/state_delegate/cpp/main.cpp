// IMPORT STANDARD LIBRARIES
#include <functional>
#include <iostream>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/base/tf/instantiateSingleton.h"  // This plus singleton.h is required
#include <pxr/base/tf/singleton.h>  // This plus instantiateSingleton.h is required
#include <pxr/usd/sdf/layerStateDelegate.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/primSpec.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/stage.h>


using Record = std::function<bool()>;


class State {
public:
    void push_back(Record const &record) {
        this->memos.push_back(record);
    }

    bool undo() {
        if (this->memos.empty()) {
            std::cout << "The undo queue is empty. There's nothing to undo.\n";
            return false;
        }

        auto function = this->memos.back();
        bool result = function();
        this->memos.pop_back();
        return result;
    };

    std::vector<Record> memos;
};


PXR_NAMESPACE_OPEN_SCOPE
TF_DECLARE_WEAK_AND_REF_PTRS(StateDelegate);


class StateDelegate : public pxr::SdfSimpleLayerStateDelegate {
public:
    static pxr::StateDelegateRefPtr New();
    StateDelegate() = default;

protected:
    bool _InvertCreateSpec(const pxr::SdfPath& path, bool inert) {
        std::cout << "Undoing " << path << '\n';

        if (!this->_GetLayer()) {
            std::cout << "Could not undo because the layer doesn't exist\n";
            // XXX : Always check that the layer exists before modifying it
            return false;
        }

        this->DeleteSpec(path, inert);

        return true;
    }

    virtual void _OnCreateSpec(const pxr::SdfPath &path, pxr::SdfSpecType type, bool inert) override {
        super::_OnCreateSpec(path, type, inert);

        std::cout << std::boolalpha;
        std::cout << "Spec was created\n";

        auto &state = pxr::TfSingleton<State>::GetInstance();
        state.push_back(
            std::bind(&StateDelegate::_InvertCreateSpec, this, path, inert
        ));

        std::cout << state.memos.empty() << '\n';
    }

    virtual void _OnSetLayer(const pxr::SdfLayerHandle &layer) override {
        super::_OnSetLayer(layer);

        std::cout << "Layer was associated with this object\n";
    }

private:
    typedef pxr::SdfSimpleLayerStateDelegate super;
};
PXR_NAMESPACE_CLOSE_SCOPE


pxr::StateDelegateRefPtr pxr::StateDelegate::New() {
    auto pointer = pxr::TfCreateRefPtr(new pxr::StateDelegate());
    return pointer;
}


int main() {
    std::cout << std::boolalpha;

    auto stage = pxr::UsdStage::CreateInMemory();
    auto root = stage->GetRootLayer();

    root->SetStateDelegate(pxr::StateDelegate::New());

    // pxr::SdfPrimSpec::New(root, "SomePrim2", pxr::SdfSpecifierDef);  XXX alternate syntax?
    stage->DefinePrim(pxr::SdfPath {"/SomePrim1"}, pxr::TfToken {"Sphere"});
    std::cout << "Is dirty " << root->GetStateDelegate()->IsDirty() << '\n';

    auto &state = pxr::TfSingleton<State>::GetInstance();
    std::cout << state.memos.empty() << '\n';
    state.undo();
    std::cout << "Is still dirty " << root->GetStateDelegate()->IsDirty() << '\n';

    return 0;
}
