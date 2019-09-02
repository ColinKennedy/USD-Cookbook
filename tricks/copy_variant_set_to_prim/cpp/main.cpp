// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/copyUtils.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/sdf/variantSetSpec.h>
#include <pxr/usd/sdf/variantSpec.h>
#include <pxr/usd/usd/stage.h>


int main() {
    auto source = pxr::SdfLayer::CreateAnonymous();
    auto root = source->GetPseudoRoot();

    auto prim = pxr::SdfPrimSpec::New(root, "SomePrim", pxr::SdfSpecifierDef);
    auto variant_set = pxr::SdfVariantSetSpec::New(prim, "SomeVariantSet");
    auto variant = pxr::SdfVariantSpec::New(variant_set, "SomeVariant");
    pxr::SdfPrimSpec::New(variant->GetPrimSpec(), "InnerPrim", pxr::SdfSpecifierDef);

    auto destination = pxr::SdfLayer::CreateAnonymous();
    pxr::SdfCopySpec(
        source,
        pxr::SdfPath {"/SomePrim{SomeVariantSet=SomeVariant}"},
        destination,
        pxr::SdfPath {"/DestinationPrim"}
    );

    // XXX : Notice that we have to call `CreatePrimInLayer` here but
    // we didn't need to run it in the last example. That's because
    // in this example, the parent Prim path "/Another" doesn't
    // exist yet and has to be created before data can be copied to
    // "/Another/DestinationPrim".
    //
    // In the previous example, "/" is the parent of "/DestinationPrim".
    // And "/" always exists. So we didn't need to call
    // `CreatePrimInLayer`. But generally, you usually should.
    //
    auto destination_prim = pxr::SdfPath {"/Another/DestinationPrim"};
    pxr::SdfCreatePrimInLayer(destination, destination_prim);
    pxr::SdfCopySpec(
        source,
        pxr::SdfPath {"/SomePrim{SomeVariantSet=SomeVariant}"},
        destination,
        destination_prim
    );

    auto* result = new std::string();
    destination->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;
    result = nullptr;

    return 0;
}
