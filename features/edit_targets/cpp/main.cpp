#include <pxr/usd/usd/sphere.h>
#include <pxr/usd/usd/stage.h>


pxr::UsdStageRefPtr _make_target()
{
    auto stage = pxr::UsdStage::CreateInMemory();
    auto root = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath{"/root"}));

}

int main() {
    auto stage = pxr::UsdStage::CreateInMemory();

    return 0;
}
