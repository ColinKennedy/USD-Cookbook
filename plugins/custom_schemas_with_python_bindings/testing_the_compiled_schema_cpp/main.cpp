// IMPORT STANDARD LIBRARIES
#include <iostream>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/usd/stage.h>
#include <complex.h>
#include <simple.h>


int main() {
    auto stage = pxr::UsdStage::Open("../test.usda");

    auto prim = stage->GetPrimAtPath(pxr::SdfPath("/Simple"));
    auto simple = pxr::UsdSchemaExamplesSimple(prim);
    auto attribute = simple.GetIntAttrAttr();
    int value = 0;
    attribute.Get<int>(&value);
    std::cout << "Got a value: " << value << std::endl;
    attribute.Set(2);
    attribute.Get<int>(&value);
    std::cout << "Got a value: " << value << std::endl;

    auto cp = stage->GetPrimAtPath(pxr::SdfPath("/Complex"));
    auto complex = pxr::UsdSchemaExamplesComplex(cp);
    std::string value1 {""};
    complex.GetComplexStringAttr().Get<std::string>(&value1);
    std::cout << value1 << std::endl;

    auto* result = new std::string();
    stage->ExportToString(result);
    std::cout << *result << std::endl;
    delete result;

    return 0;
}
