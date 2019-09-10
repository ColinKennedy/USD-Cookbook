// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/ar/defaultResolverContext.h>
#include <pxr/usd/ar/resolver.h>
#include <pxr/usd/ar/resolverContextBinder.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdUtils/dependencies.h>



int main() {
    auto context = pxr::ArDefaultResolverContext({"path"});

    auto path = "some_stage.usda";
    std::cout << "The path to find: \"" << path << "\".\n";
    auto resolver = pxr::ArGetResolver();
    std::cout
        << "This path should be empty: \""
        << resolver.Resolve(path)
        << "\".\n";

    pxr::UsdStageRefPtr stage;

    {
        auto binder = pxr::ArResolverContextBinder{context};
        std::cout
            << "Now the path will actually resolve, \""
            << resolver.Resolve(path)
            << "\".\n";
        std::cout
            << "And we can even get dependency information"
            << pxr::UsdUtilsComputeAllDependencies(path)
            << "\n";

        std::cout << '\n';
        std::cout << "XXX: We can resolve any of the below relative paths in this context\n";
        std::cout << "The next 2 paths will resolve because we added `project_folder`\n";
        std::cout << resolver.Resolve("a_dependent_layer.usda") << '\n';
        std::cout << resolver.Resolve("data.json") << '\n';
        std::cout << "The next path will resolve because we added `nested_folder`\n";
        std::cout << resolver.Resolve("some_nested_layer.usda") << '\n';

        std::cout << '\n';
        stage = pxr::UsdStage::Open("some_stage.usda");
    }

    return 0;
}
