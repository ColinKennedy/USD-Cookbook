// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>
#include <regex>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/types.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


int main() {
    auto is_user_property = [&](std::string const &path) {
        static std::string const properties = "userProperties";

        // If `path` starts with "userProperties" then it's a user property
        return strncmp(path.c_str(), properties.c_str(), strlen(properties.c_str())) == 0;
    };

    auto stage = pxr::UsdStage::CreateInMemory();
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/SomeSphere"});
    auto attribute = sphere.GetPrim().CreateAttribute(
        pxr::TfToken {"userProperties:some_attribute"},
        pxr::SdfValueTypeNames->Bool,
        true
    );
    attribute.Set(false);

    auto some_attribute_that_will_not_be_printed = sphere.GetPrim().CreateAttribute(
        pxr::TfToken {"another"},
        pxr::SdfValueTypeNames->Bool,
        true
    );

    for (auto const &property : sphere.GetPrim().GetAuthoredProperties(is_user_property)) {
        std::cout << property.GetName() << " ";
    }
    std::cout << '\n';

    return 0;
}
