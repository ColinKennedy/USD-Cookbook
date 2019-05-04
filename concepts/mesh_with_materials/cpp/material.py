#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple shading tutorial.

Reference:
    https://graphics.pixar.com/usd/docs/Simple-Shading-in-USD.html

"""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD-PARTY LIBRARIES
from pxr import Kind
from pxr import Sdf
from pxr import Usd
from pxr import UsdGeom
from pxr import UsdShade


ASSETS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def attach_billboard(stage, root, name='card'):
    billboard = UsdGeom.Mesh.Define(stage, str(root.GetPath()) + '/' + name)
    billboard.CreatePointsAttr([(-430, -145, 0), (430, -145, 0), (430, 145, 0), (-430, 145, 0)])
    billboard.CreateFaceVertexCountsAttr([4])
    billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
    billboard.CreateExtentAttr([(-430, -145, 0), (430, 145, 0)])
    texCoords = billboard.CreatePrimvar(
        "st",
        Sdf.ValueTypeNames.TexCoord2fArray,
        UsdGeom.Tokens.varying,
    )
    texCoords.Set(
        [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1),
        ],
    )
    return billboard


def attach_surface_shader(stage, material, path):
    shader = UsdShade.Shader.Define(stage, path)
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

    material.CreateSurfaceOutput().ConnectToSource(shader, "surface")

    return shader


def attach_texture(
        stage,
        shader,
        material_path,
        reader_name='stdReader',
        shader_name='diffuseTexture',
    ):
    stReader = UsdShade.Shader.Define(stage, material_path + '/' + reader_name)
    stReader.CreateIdAttr('UsdPrimvarReader_float2')

    diffuseTextureSampler = UsdShade.Shader.Define(stage,material_path + '/' + shader_name)
    diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
    diffuseTextureSampler.CreateInput(
        'file',
        Sdf.ValueTypeNames.Asset,
    ).Set(os.path.join(ASSETS_DIRECTORY, "USDLogoLrg.png"))
    diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader, 'result')
    diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler, 'rgb')

    return stReader


def main():
    '''Run the main execution of the current script.'''
    stage = Usd.Stage.CreateNew('/tmp/simpleShading.usd')
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    root = UsdGeom.Xform.Define(stage, '/TexModel')
    Usd.ModelAPI(root).SetKind(Kind.Tokens.component)

    billboard = attach_billboard(stage, root)
    material = UsdShade.Material.Define(stage, str(billboard.GetPath()) + '/' + 'boardMat')
    shader = attach_surface_shader(stage, material, str(material.GetPath()) + '/' + 'PBRShader')
    reader = attach_texture(stage, shader, str(material.GetPath()))

    stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
    stInput.Set('st')

    reader.CreateInput('varname', Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

    UsdShade.MaterialBindingAPI(billboard).Bind(material)

    stage.GetRootLayer().Export('/tmp/stage.usda')


if __name__ == '__main__':
    main()
