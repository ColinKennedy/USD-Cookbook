// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/changeBlock.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/schemaRegistry.h>
#include <pxr/usd/usdGeom/xform.h>


int main() {
    auto layer = pxr::SdfLayer::CreateAnonymous();

    pxr::SdfPathSet paths {
        pxr::SdfPath {"/AndMore"},
        pxr::SdfPath {"/AnotherOne"},
        pxr::SdfPath {"/AnotherOne/AndAnother"},
        pxr::SdfPath {"/More"},
        pxr::SdfPath {"/OkayNoMore"},
        pxr::SdfPath {"/SomeSphere"},
        pxr::SdfPath {"/SomeSphere/InnerPrim"},
        pxr::SdfPath {"/SomeSphere/InnerPrim/LastOne"},
    };

    auto xform_type = pxr::UsdSchemaRegistry::GetInstance().GetPrimDefinition<pxr::UsdGeomXform>()->GetTypeName();

    for (auto const &path : paths) {
        auto prefixes = path.GetPrefixes();
        paths.insert(std::begin(prefixes), std::end(prefixes));
    }

    {
        pxr::SdfChangeBlock batcher;

        for (auto const &path : paths) {
            auto prim_spec = pxr::SdfCreatePrimInLayer(layer, path);
            prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
            prim_spec->SetTypeName(xform_type);
        }
    }

    auto* result = new std::string();
    layer->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
