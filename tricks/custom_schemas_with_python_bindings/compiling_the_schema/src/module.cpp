#include "Python.h"
#include "pxr/pxr.h"
#include "pxr/base/tf/pyModule.h"

PXR_NAMESPACE_USING_DIRECTIVE

TF_WRAP_MODULE
{
    TF_WRAP(UsdSchemaExamplesSimple);
    TF_WRAP(UsdSchemaExamplesComplex);
    TF_WRAP(UsdSchemaExamplesParamsAPI);
    TF_WRAP(UsdSchemaExamplesTokens);
}
