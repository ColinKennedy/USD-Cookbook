#include <iostream>

#include <pxr/usd/sdf/layer.h>
#include <pxr/usd/sdf/namespaceEdit.h>
#include <pxr/usd/sdf/path.h>

int main() {
    auto layer = pxr::SdfLayer::FindOrOpen("../input.usda");

    // Try everything.
    auto edit = pxr::SdfBatchNamespaceEdit();

    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/C"}, pxr::SdfPath{"/D"}});  // Prim renames
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/B"}, pxr::SdfPath{"/C"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/D"}, pxr::SdfPath{"/B"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/G"}, pxr::SdfPath{"/E/G"}});  // Prim reparents
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/H"}, pxr::SdfPath{"/E/F/H"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/I"}, pxr::SdfPath{"/E/H"}});  // Prim reparent/rename
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/J"}, pxr::SdfPath{"/L/J"}});  // Prim reparent
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/L/J/K"}, pxr::SdfPath{"/K"}});  // Prim reparent from under a reparented prim
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/X"}, pxr::SdfPath::EmptyPath()});  // Prim remove
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/E"}, pxr::SdfPath::EmptyPath()});  // Prim with descendants remove

    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.c"}, pxr::SdfPath{"/P.d"}});  // Prim property renames
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.b"}, pxr::SdfPath{"/P.c"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.d"}, pxr::SdfPath{"/P.b"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.g"}, pxr::SdfPath{"/Q.g"}});  // Prim property reparents
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.h"}, pxr::SdfPath{"/Q/R.h"}});
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.i"}, pxr::SdfPath{"/Q.h"}});  // Prim property reparent/rename
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/P.x"}, pxr::SdfPath::EmptyPath()});  // Prim property remove

    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/S"}, pxr::SdfPath{"/T"}});  // Rename prim used in targets

    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/V{v=one}U"}, pxr::SdfPath{"/V{v=two}W/U"}});  // Variant prim reparent/rename
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/V{v=two}W"}, pxr::SdfPath::EmptyPath()});  // Variant prim remove
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/V{v=one}.u"}, pxr::SdfPath{"/V{v=two}.u"}});  // Variant property reparent/rename
    edit.Add(pxr::SdfNamespaceEdit{pxr::SdfPath{"/V{v=two}.w"}, pxr::SdfPath::EmptyPath()});  // Variant property remove

    auto* before = new std::string();
    layer->ExportToString(before);

    std::cout << std::boolalpha;
    auto result = layer->CanApply(edit);
    std::cout << "Will applying this layer fail? " << (result == pxr::SdfNamespaceEditDetail::Result::Error) << '\n';
    assert(layer->Apply(edit) && "The edit failed");

    auto* after = new std::string();
    layer->ExportToString(after);

    std::cout << (before == after) << '\n';

    delete before;
    before = nullptr;
    delete after;
    after = nullptr;

    return 0;
}
