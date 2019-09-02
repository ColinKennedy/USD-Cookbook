// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/debug.h>
#include <pxr/base/tf/diagnostic.h>
#include <pxr/usd/usd/stage.h>


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

    // XXX : Here's some code that cannot be done in the Python version
    // 1 - Defining your own debug symbol
    //
    std::cout << "My custom symbol " << pxr::TfDebug::GetDebugSymbolDescription("MY_DEBUG_SYMBOL") << '\n';
    pxr::TfDebug::SetDebugSymbolsByName("MY_DEBUG_SYMBOL", true);
    TF_DEBUG_MSG(MY_DEBUG_SYMBOL, "Some debug message\n");

    // 2 - debug profiling. Just add a scope to time and a message, for clarity
    {
        TF_DEBUG_TIMED_SCOPE(MY_DEBUG_SYMBOL, "Some timed information\n");
    }

    // 3 - TF_AXIOM, an asset macro that must always be true
    // there are also other versions, such as `TF_DEV_AXIOM` and `TF_VERIFY`
    //
    TF_AXIOM(true);  // USD seg-faults if the expression in TF_AXIOM is ever false
}

PXR_NAMESPACE_CLOSE_SCOPE


int main() {
    pxr::test();
    return 0;
}
