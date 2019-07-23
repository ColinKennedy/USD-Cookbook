// IMPORT STANDARD LIBRARIES
#include <cstdio>
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/references.h>
#include <pxr/usd/usd/stage.h>


#ifdef WINDOWS
#include <direct.h>
#define GetCurrentDir _getcwd
#else
#include <unistd.h>
#define GetCurrentDir getcwd
#endif
#include<iostream>


std::string get_current_working_directory( void ) {
  char buff[FILENAME_MAX];
  GetCurrentDir( buff, FILENAME_MAX );
  std::string current_working_dir(buff);

  return current_working_dir;
}


static std::string CURRENT_DIRECTORY = get_current_working_directory();
static std::string PARENT_DIRECTORY = CURRENT_DIRECTORY.substr(0, CURRENT_DIRECTORY.find_last_of("/\\"));


void add_prim_from_target(pxr::UsdStageRefPtr stage, pxr::UsdStagePtr const &target, pxr::SdfPath prim_path=pxr::SdfPath()) {
    pxr::UsdPrim prim;

    if (prim_path.IsEmpty()) {
        auto default_prim = target->GetDefaultPrim();

        if (!default_prim.IsValid()) {
            auto default_prim_path = pxr::SdfPath(target->GetRootLayer()->GetDefaultPrim());
            prim = target->GetPrimAtPath(default_prim_path);
        }
    } else {
        prim = target->GetPrimAtPath(prim_path);
    }

    if (!prim.IsValid()) {
        std::ostringstream out;
        out << "Prim path \"" << prim_path.GetString() << "%s\" could not be found and there is not "
            "default Prim to fall back on.";

        throw out.str();
    }

    pxr::UsdPrim created_prim;

    switch (prim.GetSpecifier()) {
        case pxr::SdfSpecifierClass:
            created_prim = stage->CreateClassPrim(prim.GetPath());

            break;
        case pxr::SdfSpecifierDef:
            created_prim = stage->DefinePrim(prim.GetPath(), prim.GetTypeName());

            break;
        case pxr::SdfSpecifierOver:
            created_prim = stage->OverridePrim(prim.GetPath());

            break;
        default:
            throw "Invalid specifier found.";
    }

    created_prim.GetReferences().AddReference(
        target->GetRootLayer()->GetIdentifier(),
        prim.GetPath()
    );
}


pxr::UsdStagePtr create_basic_stage() {
    auto stage = pxr::UsdStage::Open(PARENT_DIRECTORY + "/main.usda");

    return stage;
}

int main() {
    auto base = create_basic_stage();
    auto stage = pxr::UsdStage::CreateInMemory();
    add_prim_from_target(stage, base);

    return 0;
}
