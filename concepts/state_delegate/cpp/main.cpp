// IMPORT STANDARD LIBRARIES
#include <functional>
#include <iostream>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/layerStateDelegate.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/primSpec.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/stage.h>


using Record = std::function<bool()>;


class StateSingleton {
    public:
        void operator=(StateSingleton const&) = delete;

        static StateSingleton &get() {
            static StateSingleton instance;
            return instance;
        }

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

    private:
        StateSingleton() {}
        std::vector<Record> memos;
};


PXR_NAMESPACE_OPEN_SCOPE
TF_DECLARE_WEAK_AND_REF_PTRS(StateDelegate);


class StateDelegate : public pxr::SdfSimpleLayerStateDelegate {
    public:
        static pxr::StateDelegateRefPtr New();

    protected:
        bool _InvertCreateSpec(const pxr::SdfPath& path, bool inert) {
            std::cout << "Undoing" << path << '\n';

            if (!this->_GetLayer()) {
                std::cout << "Could not undo because the layer doesn't exist\n";
                // XXX : Always check that the layer exists before modifying it
                return false;
            }

            this->DeleteSpec(path, inert);
            return true;
        }

        virtual void _OnCreateSpec(const pxr::SdfPath &path, pxr::SdfSpecType type, bool inert) override {
            std::cout << "Spec was created\n";
            this->state.push_back(
                std::bind(
                    &StateDelegate::_InvertCreateSpec,
                    this,
                    path,
                    inert
                )
            );
        }
        virtual void _OnSetLayer(const pxr::SdfLayerHandle &layer) override {
            std::cout << "Layer was associated with this object\n";
        }

    private:
        typedef pxr::SdfSimpleLayerStateDelegate super;
        StateSingleton state = StateSingleton::get();
};
PXR_NAMESPACE_CLOSE_SCOPE


pxr::StateDelegateRefPtr pxr::StateDelegate::New() {
    auto pointer = pxr::TfCreateRefPtr(new pxr::StateDelegate());
    return pointer;
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto root = stage->GetRootLayer();

    root->SetStateDelegate(pxr::StateDelegate::New());

    // XXX : Once the delegate is set, you can author PrimSpecs any way you'd like
    // either way, the delegate will still get triggered
    //
    stage->DefinePrim(pxr::SdfPath {"/SomePrim1"}, pxr::TfToken {"Sphere"});
    pxr::SdfPrimSpec::New(root, "SomePrim2", pxr::SdfSpecifierDef);

    std::cout << std::boolalpha;
    std::cout << "Is dirty " << root->GetStateDelegate()->IsDirty() << '\n';

    auto state = StateSingleton::get();
    state.undo();
    state.undo();
    state.undo();

    std::cout << "Is still dirty " << root->GetStateDelegate()->IsDirty() << '\n';

    return 0;
}
