// IMPORT STANDARD LIBRARIES
#include <algorithm>
#include <iostream>
#include <stdio.h>
#include <string>
#include <unistd.h>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/ar/defaultResolverContext.h>
#include <pxr/usd/ar/resolver.h>
#include <pxr/usd/ar/resolverContextBinder.h>
#include <pxr/usd/sdf/assetPath.h>
#include <pxr/usd/sdf/layerUtils.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>
#include <pxr/usd/usdUtils/dependencies.h>


std::ostream& operator<<(
    std::ostream& stream,
    std::vector<std::string> const &strings
)
{
    stream << "[";

    if (strings.empty()) {
        stream << "]";
        return stream;
    }

    for (auto const string : strings) {
        stream << '"' << string << "\", ";
    }

    stream << "]";

    return stream;
}


std::ostream& operator<<(
    std::ostream& stream,
    std::vector<pxr::SdfLayerRefPtr> const &layers
)
{
    stream << "[";

    if (layers.empty()) {
        stream << "]";
        return stream;
    }

    for (auto const layer : layers) {
        stream << '"' << layer->GetRealPath() << "\", ";
    }

    stream << "]";

    return stream;
}


int main() {
    auto directory = std::string{get_current_dir_name()};  // Reference: http://man7.org/linux/man-pages/man3/getcwd.3.html
    auto project_folder = directory + "/project_folder";
    auto nested_folder = project_folder + "/nested";
    auto context = pxr::ArDefaultResolverContext({project_folder, nested_folder});

    auto path = "some_stage.usda";
    std::cout << "The path to find: \"" << path << "\".\n";
    auto& resolver = pxr::ArGetResolver();
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

        std::vector<pxr::SdfLayerRefPtr> layers;
        std::vector<std::string> assets;
        std::vector<std::string> unresolved;
        pxr::UsdUtilsComputeAllDependencies(pxr::SdfAssetPath{path}, &layers, &assets, &unresolved);
        std::cout
            << "And we can even get dependency information "
            << "(" << layers << ", " << assets << ", " << unresolved << ")\n";

        std::cout << '\n';
        std::cout << "XXX: We can resolve any of the below relative paths in this context\n";
        std::cout << "The next 2 paths will resolve because we added `project_folder`\n";
        std::cout << resolver.Resolve("a_dependent_layer.usda") << '\n';
        std::cout << resolver.Resolve("data.json") << '\n';
        std::cout << "The next path will resolve because we added `nested_folder`\n";
        std::cout << resolver.Resolve("some_nested_layer.usda") << '\n';

        std::cout << '\n';
        // This line will produce a warning about
        // Th@some_nested_layer.usda@ e reason is because that relative
        // Thpath is relative to the current USD layer and has nothing
        // Thto do with our ArDefaultResolverContext.
        //
        stage = pxr::UsdStage::Open(path);
        std::cout << "ID " << stage->GetRootLayer()->GetIdentifier() << '\n';
        std::cout << "path " << stage->GetRootLayer()->GetRealPath() << '\n';
    }

    std::cout << '\n';
    std::cout
        <<
            "XXX: But if we try to query information from the paths, that "
            "doesn't work. You might expect SomePrim and SomePrim2 to have different "
            "radius values but they are both \"20\" because the asset paths in USD layers "
            "resolve the path based on the USD layer's current position\n";
    auto sphere = pxr::UsdGeomSphere{stage->GetPrimAtPath(pxr::SdfPath{"/SomePrim"})};
    double radius;
    sphere.GetRadiusAttr().Get(&radius);
    std::cout << radius << '\n';

    sphere = pxr::UsdGeomSphere{stage->GetPrimAtPath(pxr::SdfPath{"/SomePrim2"})};
    sphere.GetRadiusAttr().Get(&radius);
    std::cout << radius << '\n';
    sphere = pxr::UsdGeomSphere{stage->GetPrimAtPath(pxr::SdfPath{"/SomePrim3"})};
    sphere.GetRadiusAttr().Get(&radius);
    std::cout << "This will be None, because @some_nested_layer.usda does not resolve: \"" << radius << "\".\n" << '\n';

    return 0;
}
