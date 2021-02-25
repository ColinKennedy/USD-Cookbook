// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


void _run_resolution_test()
{
    auto referencee = pxr::UsdStage::CreateInMemory();
    referencee->GetRootLayer().ImportFromString(
        ""
    );

}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto sphere = pxr::UsdGeomSphere::Define(stage, "/sphere");
    auto radius = sphere.CreateRadiusAttr();

    std::cout << "XXX : Starting resolution test\n";
    _run_resolution_test();
    std::cout << "XXX : Ending resolution test\n";

    std::cout << "XXX : Starting interpolation test\n";
    _run_linear_interpolation_test();
    std::cout << "XXX : Ending interpolation test\n";

    return 0;
}
