# Quick Explanation

This file will try to show important parts but still be concise. The
sections below aren't 100% of what is needed to assign materials. It is
abbreviated to save on this page's space.


### C++
```cpp
auto billboard = pxr::UsdGeomMesh::Define(stage, pxr::SdfPath("/TexModel/card"));
auto material = pxr::UsdShadeMaterial::Define(stage, pxr::SdfPath("/TexModel/card/boardMat"));
// ... more configuration details
auto shader = UsdShade.Shader.Define(stage, pxr::SdfPath("/TexModel/card/boardMat/PBRShader"));
// ... more configuration details
material.CreateSurfaceOutput().ConnectToSource(shader, pxr::TfToken("surface"));
// ... more configuration details
auto reader = pxr::UsdShadeShader::Define(stage, "/TexModel/card/boardMat/stReader");
// ... more configuration details
auto st_input = material.CreateInput(
    pxr::TfToken("frame:stPrimvarName"),
    pxr::SdfValueTypeNames->Token,
);
st_input.Set(pxr::TfToken("st"));
// ... more configuration details
reader.CreateInput(pxr::TfToken("varname"), pxr::SdfValueTypeNames->Token)
    .ConnectToSource(st_input);

pxr::UsdShadeMaterialBindingAPI(billboard).Bind(material);
```


### Python
```python
billboard = UsdGeom.Mesh.Define(stage, '/TexModel/card')
material = UsdShade.Material.Define(stage, '/TexModel/card/boardMat')
# ... more configuration details
shader = UsdShade.Shader.Define(stage, '/TexModel/card/boardMat/PBRShader')
# ... more configuration details
material.CreateSurfaceOutput().ConnectToSource(shader, "surface")
reader = UsdShade.Shader.Define(stage, '/TexModel/card/boardMat/stReader')
# ... more configuration details
st_input = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
st_input.Set('st')
# ... more configuration details
reader.CreateInput('varname', Sdf.ValueTypeNames.Token).ConnectToSource(st_input)

UsdShade.MaterialBindingAPI(billboard).Bind(material)
```


## Simple Material Assignment
### USD
```usda
#usda 1.0

def Xform "TexModel" (
    kind = "component"
)
{
    def Mesh "card"
    {
        rel material:binding = </TexModel/card/boardMat>
        point3f[] points = [ ... ]
        texCoord2f[] primvars:st = [ ... ] (
            interpolation = "varying"
        )

        def Material "boardMat"
        {
            token inputs:frame:stPrimvarName = "st"
            token outputs:surface.connect = </TexModel/card/boardMat/PBRShader.outputs:surface>

            def Shader "PBRShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor.connect = </TexModel/card/boardMat/diffuseTexture.outputs:rgb>
                " ... "
            }

            def Shader "stReader"
            {
                uniform token info:id = "UsdPrimvarReader_float2"
                token inputs:varname.connect = </TexModel/card/boardMat.inputs:frame:stPrimvarName>
                float2 outputs:result
            }

            def Shader "diffuseTexture"
            {
                uniform token info:id = "UsdUVTexture"
                asset inputs:file = @./USDLogoLrg.png@
                float2 inputs:st.connect = </TexModel/card/boardMat/stReader.outputs:result>
                float3 outputs:rgb
            }
        }
    }
}

```

## Material Assignment Using Overrides
### USD
base.usda

```usda
#usda 1.0

def Xform "TexModel" (
    kind = "component"
)
{
    def Mesh "card"
    {
        float3[] extent = [ ... ]
        texCoord2f[] primvars:st = [ ... ] (
            interpolation = "varying"
        )
    }
}
```

override.usda
```usda
#usda 1.0
(
     subLayers = [
        @./base.usda@
     ]
)


over "TexModel" {
    over "card" {
        rel material:binding = </TexModel/card/boardMat>

        def Material "boardMat"
        {
            token inputs:frame:stPrimvarName = "st"
            token outputs:surface.connect = </TexModel/card/boardMat/PBRShader.outputs:surface>

            def Shader "PBRShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor.connect = </TexModel/card/boardMat/diffuseTexture.outputs:rgb>
                token outputs:surface
            }

            def Shader "stReader"
            {
                uniform token info:id = "UsdPrimvarReader_float2"
                token inputs:varname.connect = </TexModel/card/boardMat.inputs:frame:stPrimvarName>
                float2 outputs:result
            }

            def Shader "diffuseTexture"
            {
                uniform token info:id = "UsdUVTexture"
                float2 inputs:st.connect = </TexModel/card/boardMat/stReader.outputs:result>
                float3 outputs:rgb
            }
        }
    }
}
```
