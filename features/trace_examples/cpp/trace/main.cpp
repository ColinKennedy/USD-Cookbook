// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/trace/trace.h>
#include <pxr/base/trace/reporter.h>
#include <pxr/usd/sdf/changeBlock.h>
#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/schemaRegistry.h>
#include <pxr/usd/usdGeom/xform.h>

void create_sdf_primspecs_normally()
{
    TRACE_FUNCTION();

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
}


void create_sdf_primspecs_using_change_block()
{
    TRACE_FUNCTION();

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

    for (auto const &path : paths) {
        auto prim_spec = pxr::SdfCreatePrimInLayer(layer, path);
        prim_spec->SetSpecifier(pxr::SdfSpecifierDef);
        prim_spec->SetTypeName(xform_type);
    }
}


int main() {
    std::cout << "It's not enough to just add Trace.TraceFunction or scope.\n";
    std::cout << "You must also enable a collector\n";

    create_sdf_primspecs_normally();
    create_sdf_primspecs_using_change_block();

    std::cout << "This next report will be empty\n";
    auto reporter = pxr::TraceReporter::GetGlobalReporter();
    reporter->Report(std::cout);

    std::cout << "This next report will have contents, because the collector is recorded\n";
    auto* collector = &pxr::TraceCollector::GetInstance();
    collector->SetEnabled(true);
    create_sdf_primspecs_normally();
    collector->SetEnabled(false);

    reporter->Report(std::cout);
    // reporter->ReportTimes(std::cout);  // XXX : A more concise ms timing view

    std::cout << "This final exam uses an SdfChangeBlock - it should be much faster\n";
    // XXX : On my machine, using the SdfChangeBlock was consistently 70-280 ms faster
    collector->Clear();
    reporter->ClearTree();
    collector->SetEnabled(true);
    create_sdf_primspecs_using_change_block();
    collector->SetEnabled(false);

    reporter->Report(std::cout);
    // reporter->ReportTimes(std::cout);  // XXX : A more concise ms timing view

    return 0;
}
