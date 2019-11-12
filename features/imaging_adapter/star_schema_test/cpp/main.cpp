// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <star.h>


int main() {
    auto stage = pxr::UsdStage::Open("../star_file.usda");
    auto prim = stage->GetPrimAtPath(pxr::SdfPath {"/star"});
    auto star = pxr::UsdStarStar(prim);
    prim = star.GetPrim();

    std::cout << std::boolalpha;
    std::cout << "This should print True: " << prim.IsValid() << '\n';

    return 0;
}
