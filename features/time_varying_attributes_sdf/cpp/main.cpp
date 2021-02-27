#include <iostream>
#include <string>

#include <pxr/base/vt/value.h>
#include <pxr/usd/sdf/attributeSpec.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usd/stage.h>


void as_sdf()
{
    auto layer = pxr::SdfLayer::CreateAnonymous();
    auto prim_spec = pxr::SdfCreatePrimInLayer(layer, pxr::SdfPath {"/root"});
    prim_spec->SetSpecifier(pxr::SdfSpecifierDef);

    auto attribute_spec = pxr::SdfAttributeSpec::New(
        prim_spec,
        "some_name",
        pxr::SdfValueTypeNames->Int
    );
    attribute_spec->SetCustom(true);
    attribute_spec->SetDefaultValue(pxr::VtValue{8});

    layer->SetTimeSample(attribute_spec->GetPath(), 10.5, 9);

    auto* result = new std::string();
    layer->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;
}


void as_usd()
{
    auto stage = pxr::UsdStage::CreateInMemory();
    auto prim = stage->DefinePrim(pxr::SdfPath {"/root"});
    auto attribute = prim.CreateAttribute(
        pxr::TfToken {"some_name"},
        pxr::SdfValueTypeNames->Int,
        true
    );

    attribute.Set(8);

    auto layer = stage->GetEditTarget().GetLayer();  // By default, this is `stage.GetRootLayer`
    layer->SetTimeSample(attribute.GetPath(), 10.5, 9);

    auto* result = new std::string();
    stage->GetRootLayer()->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;
}


int main() {
    as_sdf(),
    as_usd();

    return 0;
}
