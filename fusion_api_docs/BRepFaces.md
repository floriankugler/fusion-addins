# BRepFaces Object

Derived from: [Base](Base.md) Object  

## Description

BRepFace collection.

## Methods

| Name | Description |
|----|----|
| [classType](BRepFaces_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepFaces_item.md) | Function that returns the specified face using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepFaces_count.md) | The number of faces in the collection. |
| [isValid](BRepFaces_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepFaces_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ArrangeFeature.faces](ArrangeFeature_faces.md), [BaseFeature.faces](BaseFeature_faces.md), [BossFeature.faces](BossFeature_faces.md), [BoundaryFillFeature.faces](BoundaryFillFeature_faces.md), [BoxFeature.faces](BoxFeature_faces.md), [BRepBody.faces](BRepBody_faces.md), [BRepEdge.faces](BRepEdge_faces.md), [BRepFace.tangentiallyConnectedFaces](BRepFace_tangentiallyConnectedFaces.md), [BRepLump.faces](BRepLump_faces.md), [BRepShell.faces](BRepShell_faces.md), [BRepVertex.faces](BRepVertex_faces.md), [ChamferFeature.faces](ChamferFeature_faces.md), [CircularPatternFeature.faces](CircularPatternFeature_faces.md), [CoilFeature.faces](CoilFeature_faces.md), [CombineFeature.faces](CombineFeature_faces.md), [CopyPasteBody.faces](CopyPasteBody_faces.md), [CornerClosureFeature.faces](CornerClosureFeature_faces.md), [CustomFeature.faces](CustomFeature_faces.md), [CutPasteBody.faces](CutPasteBody_faces.md), [CylinderFeature.faces](CylinderFeature_faces.md), [DeleteFaceFeature.faces](DeleteFaceFeature_faces.md), [DeriveFeature.faces](DeriveFeature_faces.md), [DraftFeature.faces](DraftFeature_faces.md), [EmbossFeature.faces](EmbossFeature_faces.md), [ExtendFeature.faces](ExtendFeature_faces.md), [ExtrudeFeature.endFaces](ExtrudeFeature_endFaces.md), [ExtrudeFeature.faces](ExtrudeFeature_faces.md), [ExtrudeFeature.sideFaces](ExtrudeFeature_sideFaces.md), [ExtrudeFeature.startFaces](ExtrudeFeature_startFaces.md), [Feature.faces](Feature_faces.md), [FilletFeature.faces](FilletFeature_faces.md), [FlangeFeature.faces](FlangeFeature_faces.md), [FlatPattern.faces](FlatPattern_faces.md), [FlatPattern.sideFaces](FlatPattern_sideFaces.md), [FormFeature.faces](FormFeature_faces.md), [HemFeature.faces](HemFeature_faces.md), [HoleFeature.endFaces](HoleFeature_endFaces.md), [HoleFeature.faces](HoleFeature_faces.md), [HoleFeature.sideFaces](HoleFeature_sideFaces.md), [LoftFeature.faces](LoftFeature_faces.md), [LoftFeature.sideFaces](LoftFeature_sideFaces.md), [MeshCombineFaceGroupsFeature.faces](MeshCombineFaceGroupsFeature_faces.md), [MeshCombineFeature.faces](MeshCombineFeature_faces.md), [MeshConvertFeature.faces](MeshConvertFeature_faces.md), [MeshFeature.faces](MeshFeature_faces.md), [MeshGenerateFaceGroupsFeature.faces](MeshGenerateFaceGroupsFeature_faces.md), [MeshReduceFeature.faces](MeshReduceFeature_faces.md), [MeshRemeshFeature.faces](MeshRemeshFeature_faces.md), [MeshRemoveFeature.faces](MeshRemoveFeature_faces.md), [MeshRepairFeature.faces](MeshRepairFeature_faces.md), [MeshReverseNormalFeature.faces](MeshReverseNormalFeature_faces.md), [MeshSeparateFeature.faces](MeshSeparateFeature_faces.md), [MeshShellFeature.faces](MeshShellFeature_faces.md), [MeshSmoothFeature.faces](MeshSmoothFeature_faces.md), [MirrorFeature.faces](MirrorFeature_faces.md), [MoveFeature.faces](MoveFeature_faces.md), [OffsetFacesFeature.faces](OffsetFacesFeature_faces.md), [OffsetFeature.faces](OffsetFeature_faces.md), [PatchFeature.faces](PatchFeature_faces.md), [PathPatternFeature.faces](PathPatternFeature_faces.md), [PipeFeature.endFaces](PipeFeature_endFaces.md), [PipeFeature.faces](PipeFeature_faces.md), [PipeFeature.sideFaces](PipeFeature_sideFaces.md), [PipeFeature.startFaces](PipeFeature_startFaces.md), [RectangularPatternFeature.faces](RectangularPatternFeature_faces.md), [RefoldFeature.faces](RefoldFeature_faces.md), [RemoveFeature.faces](RemoveFeature_faces.md), [ReplaceFaceFeature.faces](ReplaceFaceFeature_faces.md), [ReverseNormalFeature.faces](ReverseNormalFeature_faces.md), [RevolveFeature.endFaces](RevolveFeature_endFaces.md), [RevolveFeature.faces](RevolveFeature_faces.md), [RevolveFeature.sideFaces](RevolveFeature_sideFaces.md), [RevolveFeature.startFaces](RevolveFeature_startFaces.md), [RibFeature.faces](RibFeature_faces.md), [RipFeature.faces](RipFeature_faces.md), [RuledSurfaceFeature.faces](RuledSurfaceFeature_faces.md), [RuleFilletFeature.faces](RuleFilletFeature_faces.md), [ScaleFeature.faces](ScaleFeature_faces.md), [ShellFeature.faces](ShellFeature_faces.md), [SilhouetteSplitFeature.faces](SilhouetteSplitFeature_faces.md), [SphereFeature.faces](SphereFeature_faces.md), [SplitBodyFeature.faces](SplitBodyFeature_faces.md), [SplitFaceFeature.faces](SplitFaceFeature_faces.md), [StitchFeature.faces](StitchFeature_faces.md), [SurfaceDeleteFaceFeature.faces](SurfaceDeleteFaceFeature_faces.md), [SweepFeature.endFaces](SweepFeature_endFaces.md), [SweepFeature.faces](SweepFeature_faces.md), [SweepFeature.sideFaces](SweepFeature_sideFaces.md), [SweepFeature.startFaces](SweepFeature_startFaces.md), [TessellateFeature.faces](TessellateFeature_faces.md), [ThickenFeature.faces](ThickenFeature_faces.md), [ThreadFeature.faces](ThreadFeature_faces.md), [TorusFeature.faces](TorusFeature_faces.md), [TrimFeature.faces](TrimFeature_faces.md), [UnfoldFeature.faces](UnfoldFeature_faces.md), [UnstitchFeature.faces](UnstitchFeature_faces.md), [UntrimFeature.faces](UntrimFeature_faces.md), [VolumetricCustomFeature.faces](VolumetricCustomFeature_faces.md), [VolumetricModelToMeshFeature.faces](VolumetricModelToMeshFeature_faces.md), [WebFeature.faces](WebFeature_faces.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

