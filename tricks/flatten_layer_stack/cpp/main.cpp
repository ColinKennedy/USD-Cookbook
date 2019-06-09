// IMPORT STANDARD LIBRARIES
#include <algorithm>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdGeom/xform.h>
#include <pxr/usd/usdUtils/flattenLayerStack.h>
#include <pxr/usd/usdUtils/stitch.h>


int main() {
    // Initialize the stage and layers
    auto stage = pxr::UsdStage::CreateInMemory();
    pxr::UsdGeomXform::Define(stage, pxr::SdfPath {"/SomeTransform"});
    pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/SomeTransform/SomeSphere"});
    auto anonymous1 = pxr::UsdStage::CreateInMemory();
    anonymous1->DefinePrim(pxr::SdfPath {"/SomeItemInAnonymous"});
    auto anonymous2 = pxr::UsdStage::CreateInMemory();
    anonymous2->DefinePrim(pxr::SdfPath {"/SomethingElseThatIsInAnotherLayer"});

    // Add some composition arcs that target the anonymous layers
    auto prim = stage->GetPrimAtPath(pxr::SdfPath {"/SomeTransform/SomeSphere"});
    prim.GetReferences().AddReference(
        anonymous1->GetRootLayer()->GetIdentifier(), pxr::SdfPath {"/SomeItemInAnonymous"}
    );
    prim.GetReferences().AddReference(
        anonymous1->GetRootLayer()->GetIdentifier(), pxr::SdfPath {"/SomethingElseThatIsInAnotherLayer"}
    );

    // XXX : Here we are using `FlattenLayerStack` to replace the
    // authored, anonymous assetPath arguments with nothing because we
    // are about to merge the anonymous layer(s) into the stage anyway,
    // so the paths will just refer to the current USD stage.
    //
    auto roots = std::vector<pxr::SdfLayerHandle> {};
    roots.reserve(2);
    roots.push_back(anonymous1->GetRootLayer());
    roots.push_back(anonymous2->GetRootLayer());
    std::vector<std::string> identifiers;
    identifiers.reserve(roots.size());
    for (auto const &root : roots) {
        identifiers.push_back(root->GetIdentifier());
    }

    pxr::UsdUtilsResolveAssetPathFn anonymous_path_remover =
        [&identifiers](pxr::SdfLayerHandle const &sourceLayer, std::string const &path) {
            if (std::find(std::begin(identifiers), std::end(identifiers), path) != std::end(identifiers)) {
                return std::string {};
            }

            return std::string {path.c_str()};
        };

    auto layer = pxr::UsdUtilsFlattenLayerStack(stage, anonymous_path_remover);

    // XXX : Merge each anonymous layer that was listed in `identifiers`
    // into the current stage. That way, the references that were created
    // will not break.
    //
    for (auto const &root : roots) {
        pxr::UsdUtilsStitchLayers(layer, root);
    }

    auto* result = new std::string();
    layer->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
