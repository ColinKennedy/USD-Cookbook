#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple shading tutorial.

Reference:
    https://graphics.pixar.com/usd/docs/Simple-Shading-in-USD.html

"""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Kind, Sdf, Usd, UsdGeom, UsdShade

ASSETS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def attach_billboard(stage, root, name="card"):
    billboard = UsdGeom.Mesh.Define(stage, str(root.GetPath()) + "/" + name)
    billboard.CreatePointsAttr(
        [(-430, -145, 0), (430, -145, 0), (430, 145, 0), (-430, 145, 0)]
    )
    billboard.CreateFaceVertexCountsAttr([4])
    billboard.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
    billboard.CreateExtentAttr([(-430, -145, 0), (430, 145, 0)])
    texCoords = billboard.CreatePrimvar(
        "st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.varying
    )
    texCoords.Set([(0, 0), (1, 0), (1, 1), (0, 1)])
    return billboard


def attach_surface_shader(stage, material, path):
    shader = UsdShade.Shader.Define(stage, path)
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material.CreateSurfaceOutput().ConnectToSource(shader, "surface")

    return shader


def attach_texture(
    stage, shader, material_path, reader_name="stReader", shader_name="diffuseTexture"
):
    reader = UsdShade.Shader.Define(stage, material_path + "/" + reader_name)
    reader.CreateIdAttr("UsdPrimvarReader_float2")

    diffuseTextureSampler = UsdShade.Shader.Define(
        stage, material_path + "/" + shader_name
    )
    diffuseTextureSampler.CreateIdAttr("UsdUVTexture")
    diffuseTextureSampler.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(
        os.path.join(ASSETS_DIRECTORY, "USDLogoLrg.png")
    )
    diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(
        reader, "result"
    )
    diffuseTextureSampler.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
        diffuseTextureSampler, "rgb"
    )

    return reader


def main():
    """Run the main execution of the current script."""
    stage = Usd.Stage.CreateInMemory()
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    root = UsdGeom.Xform.Define(stage, "/TexModel")
    Usd.ModelAPI(root).SetKind(Kind.Tokens.component)

    billboard = attach_billboard(stage, root)
    material = UsdShade.Material.Define(
        stage, str(billboard.GetPath()) + "/" + "boardMat"
    )
    shader = attach_surface_shader(
        stage, material, str(material.GetPath()) + "/" + "PBRShader"
    )
    reader = attach_texture(stage, shader, str(material.GetPath()))

    st_input = material.CreateInput("frame:stPrimvarName", Sdf.ValueTypeNames.Token)
    st_input.Set("st")

    reader.CreateInput("varname", Sdf.ValueTypeNames.Token).ConnectToSource(st_input)

    UsdShade.MaterialBindingAPI(billboard).Bind(material)

    print(stage.GetRootLayer().ExportToString())


if __name__ == "__main__":
    main()
