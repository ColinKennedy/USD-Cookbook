// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include "pxr/base/tf/debug.h"
#include "pxr/usd/usd/stage.h"


// TF_DEBUG(PXRUSDMAYAGL_SHAPE_ADAPTER_BUCKETING).Msg(
//     "            shape adapter: %p\n",
//     shapeAdapter);
PXR_NAMESPACE_OPEN_SCOPE
TF_DEBUG_CODES(
    MY_DEBUG_SYMBOL
);

TF_REGISTRY_FUNCTION(TfDebug)
{
    TF_DEBUG_ENVIRONMENT_SYMBOL(MY_DEBUG_SYMBOL, "Some description for the symbol.");
}


void test() {
    pxr::TfDebug::SetOutputFile(stderr);

    auto stage = pxr::UsdStage::CreateInMemory();
    // XXX : The actual symbols are defined in C++ across many files.
    // You can query them using `Tf.Debug.GetDebugSymbolNames()` or by
    // searching for files that call the `TF_DEBUG_CODES` macro in C++.
    // (Usually this is in files named "debugCodes.h").
    //
    auto symbols = pxr::TfDebug::GetDebugSymbolNames();

    // XXX : Check if debug symbols are enabled
    // (on my machine, they're all False by default)
    //
    for (auto const &symbol : symbols) {
        std::cout << symbol << '\n';
    }

    // XXX : Here's a full description of everything
    std::cout << "Description start\n";
    std::cout << pxr::TfDebug::GetDebugSymbolDescriptions() << '\n';
    std::cout << "Description end\n";

    // XXX : Enable change processing so we can see something happening
    // You can also use glob matching. Like "USD_*" to enable many flags
    // at once.
    //
    pxr::TfDebug::SetDebugSymbolsByName("USD_CHANGES", true);
    stage->DefinePrim(pxr::SdfPath {"/SomePrim"});

    // XXX : Here's some stuff that isn't in the Python version
    std::cout << "My custom symbol " << pxr::TfDebug::GetDebugSymbolDescription("MY_DEBUG_SYMBOL") << '\n';
    pxr::TfDebug::SetDebugSymbolsByName("MY_DEBUG_SYMBOL", true);
    TF_DEBUG_MSG(MY_DEBUG_SYMBOL, "whatever");
// - profiling? TF_DEBUG_TIMED_SCOPE()
// TF_AXIOM


}

PXR_NAMESPACE_CLOSE_SCOPE


int main() {
    pxr::test();
    return 0;
}
