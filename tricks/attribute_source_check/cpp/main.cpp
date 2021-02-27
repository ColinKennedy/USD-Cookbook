// IMPORT STANDARD LIBRARIES
#include <cstdio>
#include <iostream>
#include <tuple>
#include <vector>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/stringUtils.h>
#include <pxr/usd/sdf/layerOffset.h>
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/sdf/reference.h>
#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/resolveInfo.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/sphere.h>


struct _Time
{
    int time_code;
    double expected_value;
    pxr::UsdResolveInfoSource expected_resolve;
};


bool is_interpolated(pxr::UsdAttribute const &attribute, double frame)
{

    double lower;
    double upper;
    bool has_time_samples;

    attribute.GetBracketingTimeSamples(frame, &lower, &upper, &has_time_samples);

    // XXX : `lower != upper` means "you cannot be interpolating
    // between two values if there is only one value.
    //
    return (has_time_samples && lower != upper && lower != frame);
}


// Reference: https://stackoverflow.com/a/1489873/3626104
template <class T>
int _get_digits_count(T number)
{
    int digits = 0;

    if (number < 0.0) {
        digits = 1; // remove this line if '-' counts as a digit
    }

    while (number) {
        number /= 10.0;
        digits++;
    }
    return digits;
}


void _run_resolution_test()
{
    auto referencee = pxr::UsdStage::CreateInMemory();
    referencee->GetRootLayer()->ImportFromString(
        {
            R"(#usda 1.0
            (
                defaultPrim = "root"
            )

            def Scope "root"
            {
                def Sphere "sphere"
                {
                    double radius = 2
                    double radius.timeSamples = {
                        10: 10,
                        40: 40,
                    }
                }
            }
            )"
        }
    );

    auto referencer = pxr::UsdStage::CreateInMemory();
    auto root = referencer->DefinePrim(pxr::SdfPath {"/root"});

    root.GetReferences().AddReference(
        pxr::SdfReference(
            referencee->GetRootLayer()->GetIdentifier(),
            pxr::SdfPath(),
            pxr::SdfLayerOffset {5 /* offset */, 2 /* scale */}
        )
    );

    auto sphere = pxr::UsdGeomSphere(referencer->GetPrimAtPath(pxr::SdfPath {"/root/sphere"}));
    auto radius = sphere.GetRadiusAttr();

    std::vector<_Time> times {
        {10, 10.0, pxr::UsdResolveInfoSourceTimeSamples},
        {20, 10.0, pxr::UsdResolveInfoSourceTimeSamples},
        {25, 10.0, pxr::UsdResolveInfoSourceTimeSamples},
        {30, 12.5, pxr::UsdResolveInfoSourceTimeSamples},
        {55, 25.0, pxr::UsdResolveInfoSourceTimeSamples},
        {85, 40.0, pxr::UsdResolveInfoSourceTimeSamples},
    };

    std::string template_ = \
R"(Expected Value: "%f"
Actual Value: "%f"
Expected Resolve: "%s"
Actual Resolve: "%s")";

    for (auto const &entry : times)
    {
        std::cout << "Time Start: \"" << entry.time_code << "\"\n";

        double actual_value;
        radius.Get(&actual_value, entry.time_code);
        auto expected_resolve = pxr::TfStringify(entry.expected_resolve);
        auto actual_resolve = radius.GetResolveInfo(entry.time_code).GetSource();
        auto actual_resolve_text = pxr::TfStringify(actual_resolve);

        auto size = template_.size() \
            + _get_digits_count(entry.expected_value)
            + _get_digits_count(actual_value)
            + expected_resolve.size()
            + actual_resolve_text.size()
        ;
        char *buffer = new char[size];

        snprintf(
            buffer,
            size,
            template_.c_str(),
            entry.expected_value,
            actual_value,
            expected_resolve.c_str(),
            actual_resolve_text.c_str()
        );
        std::cout << buffer << "\n";
        delete[] buffer;
        buffer = nullptr;

        std::cout << "Time End: \"" << entry.time_code << "\"\n";
    }
}

void _run_linear_interpolation_test()
{
    auto stage = pxr::UsdStage::CreateInMemory();
    stage->GetRootLayer()->ImportFromString(
        {
            R"(#usda 1.0

            def Scope "root"
            {
                int foo = 8
                int foo.timeSamples = {
                    5: 10,
                    20: 40,
                }
            }
            )"
        }
    );

    auto prim = stage->GetPrimAtPath(pxr::SdfPath {"/root"});
    auto attribute = prim.GetAttribute(pxr::TfToken {"foo"});

    std::vector<int> times = {-5, 3, 5, 10, 15, 20, 25};

    for (auto time_code : times)
    {
        auto value = is_interpolated(attribute, static_cast<double>(time_code));
        std::cout << "Time \"" << time_code << "\", Value \"" << value << "\"\n";
    }
}


int main() {
    auto stage = pxr::UsdStage::CreateInMemory();
    auto sphere = pxr::UsdGeomSphere::Define(stage, pxr::SdfPath {"/sphere"});
    auto radius = sphere.CreateRadiusAttr();

    std::cout << "XXX : Starting resolution test\n";
    _run_resolution_test();
    std::cout << "XXX : Ending resolution test\n";

    std::cout << "XXX : Starting interpolation test\n";
    std::cout << std::boolalpha;
    _run_linear_interpolation_test();
    std::cout << "XXX : Ending interpolation test\n";

    std::cout << "Radius will print ~1.0 and UsdResolveInfoSourceFallback\n";
    double value;
    radius.Get(&value);
    printf("%f\n", value);
    std::cout << pxr::TfStringify(radius.GetResolveInfo().GetSource()) << "\n";
    std::cout << "Radius will print ~5.0 and UsdResolveInfoSourceDefault\n";
    radius.Set(5.0);
    radius.Get(&value);
    printf("%f\n", value);
    std::cout << pxr::TfStringify(radius.GetResolveInfo().GetSource()) << "\n";

    return 0;
}
