// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/reference.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/xform.h>


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();

    pxr::SdfPath master {"/MyPrim"};

    std::vector<pxr::SdfPath> instances = {
        pxr::SdfPath {"/AnotherPath/InnerPrim1"},
        pxr::SdfPath {"/AnotherPath/InnerPrim2"},
    };
    std::vector<pxr::SdfPath> paths {
        pxr::SdfPath {"/AnotherPath"},
        pxr::SdfPath {"/MyPrim/SomePrim"},
        master,
    };

    for (auto const &path : paths) {
        pxr::UsdGeomXform::Define(stage, path);
    }
    for (auto const &path : instances) {
        pxr::UsdGeomXform::Define(stage, path);
    }

    for (auto const &instance : instances) {
        auto prim = stage->GetPrimAtPath(instance);
        prim.GetReferences().AddReference(
            stage->GetRootLayer()->GetIdentifier(),
            pxr::SdfPath {"/MyPrim"}
        );
        prim.SetInstanceable(true);
    }

    try {
        stage->DefinePrim(pxr::SdfPath {"/AnotherPrim/InnerPrim1/SomePrimThatWillNotExist"});
    } catch (...) {
        // XXX : Interestingly, this doesn't raise an exception but it does in Python
        // TODO : Look into why this doesn't raise
        //
        std::cout << "THIS EXCEPTION WILL NOT BE RAISED\n";
    }

    stage->DefinePrim(pxr::SdfPath {"/AnotherPrim/InnerPrim1"}).SetInstanceable(false);
    // XXX : We broke the instance so now it will not raise an exception
    // If you want to, you can also do `if not prim.IsInstance(): stage.DefinePrim`
    //
    stage->DefinePrim(pxr::SdfPath {"/AnotherPrim/InnerPrim1/SomePrimThatWillExist"});

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
