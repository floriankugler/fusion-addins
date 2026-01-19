# BRepBodies Object

Derived from: [Base](Base.md) Object  

## Description

The BRepBodies collection provides access to all of the B-Rep bodies within a component.

## Methods

| Name | Description |
| --- | --- |
| [add](BRepBodies_add.md) | Creates a new BRepBody object. The input can be a persisted or transient BRepBody and the result is a persisted BRepBody. In a direct modeling design, the BRepBody is created within the component the BRepBodies collection was obtained from. In a parametric modeling design, the new BRepBody is created within the specified Base Feature. Because of a current limitation, if you want to create a BRepBody in a parametric model, you must first call the edit method of the base feature, then use the add method to create the body, and finally call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [classType](BRepBodies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepBodies_item.md) | Function that returns the specified body using an index into the collection. |
| [itemByName](BRepBodies_itemByName.md) | Returns a specific body using the name of the body within the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepBodies_count.md) | Returns the number of bodies in the collection. |
| [isValid](BRepBodies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepBodies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ArrangeFeature.bodies](ArrangeFeature_bodies.md), [BaseComponent.bRepBodies](BaseComponent_bRepBodies.md), [BaseFeature.bodies](BaseFeature_bodies.md), [BossFeature.bodies](BossFeature_bodies.md), [BoundaryFillFeature.bodies](BoundaryFillFeature_bodies.md), [BoxFeature.bodies](BoxFeature_bodies.md), [ChamferFeature.bodies](ChamferFeature_bodies.md), [CircularPatternFeature.bodies](CircularPatternFeature_bodies.md), [CoilFeature.bodies](CoilFeature_bodies.md), [CombineFeature.bodies](CombineFeature_bodies.md), [Component.bRepBodies](Component_bRepBodies.md), [CopyPasteBody.bodies](CopyPasteBody_bodies.md), [CornerClosureFeature.bodies](CornerClosureFeature_bodies.md), [CustomFeature.bodies](CustomFeature_bodies.md), [CutPasteBody.bodies](CutPasteBody_bodies.md), [CylinderFeature.bodies](CylinderFeature_bodies.md), [DeleteFaceFeature.bodies](DeleteFaceFeature_bodies.md), [DeriveFeature.bodies](DeriveFeature_bodies.md), [DraftFeature.bodies](DraftFeature_bodies.md), [EmbossFeature.bodies](EmbossFeature_bodies.md), [ExtendFeature.bodies](ExtendFeature_bodies.md), [ExtrudeFeature.bodies](ExtrudeFeature_bodies.md), [Feature.bodies](Feature_bodies.md), [FilletFeature.bodies](FilletFeature_bodies.md), [FlangeFeature.bodies](FlangeFeature_bodies.md), [FlatPattern.bodies](FlatPattern_bodies.md), [FlatPatternComponent.bRepBodies](FlatPatternComponent_bRepBodies.md), [FormFeature.bodies](FormFeature_bodies.md), [HemFeature.bodies](HemFeature_bodies.md), [HoleFeature.bodies](HoleFeature_bodies.md), [LoftFeature.bodies](LoftFeature_bodies.md), [MeshCombineFaceGroupsFeature.bodies](MeshCombineFaceGroupsFeature_bodies.md), [MeshCombineFeature.bodies](MeshCombineFeature_bodies.md), [MeshConvertFeature.bodies](MeshConvertFeature_bodies.md), [MeshFeature.bodies](MeshFeature_bodies.md), [MeshGenerateFaceGroupsFeature.bodies](MeshGenerateFaceGroupsFeature_bodies.md), [MeshReduceFeature.bodies](MeshReduceFeature_bodies.md), [MeshRemeshFeature.bodies](MeshRemeshFeature_bodies.md), [MeshRemoveFeature.bodies](MeshRemoveFeature_bodies.md), [MeshRepairFeature.bodies](MeshRepairFeature_bodies.md), [MeshReverseNormalFeature.bodies](MeshReverseNormalFeature_bodies.md), [MeshSeparateFeature.bodies](MeshSeparateFeature_bodies.md), [MeshShellFeature.bodies](MeshShellFeature_bodies.md), [MeshSmoothFeature.bodies](MeshSmoothFeature_bodies.md), [MirrorFeature.bodies](MirrorFeature_bodies.md), [MoveFeature.bodies](MoveFeature_bodies.md), [Occurrence.bRepBodies](Occurrence_bRepBodies.md), [OffsetFacesFeature.bodies](OffsetFacesFeature_bodies.md), [OffsetFeature.bodies](OffsetFeature_bodies.md), [PatchFeature.bodies](PatchFeature_bodies.md), [PathPatternFeature.bodies](PathPatternFeature_bodies.md), [PipeFeature.bodies](PipeFeature_bodies.md), [RectangularPatternFeature.bodies](RectangularPatternFeature_bodies.md), [RefoldFeature.bodies](RefoldFeature_bodies.md), [RemoveFeature.bodies](RemoveFeature_bodies.md), [ReplaceFaceFeature.bodies](ReplaceFaceFeature_bodies.md), [ReverseNormalFeature.bodies](ReverseNormalFeature_bodies.md), [RevolveFeature.bodies](RevolveFeature_bodies.md), [RibFeature.bodies](RibFeature_bodies.md), [RipFeature.bodies](RipFeature_bodies.md), [RuledSurfaceFeature.bodies](RuledSurfaceFeature_bodies.md), [RuleFilletFeature.bodies](RuleFilletFeature_bodies.md), [ScaleFeature.bodies](ScaleFeature_bodies.md), [ShellFeature.bodies](ShellFeature_bodies.md), [SilhouetteSplitFeature.bodies](SilhouetteSplitFeature_bodies.md), [SphereFeature.bodies](SphereFeature_bodies.md), [SplitBodyFeature.bodies](SplitBodyFeature_bodies.md), [SplitFaceFeature.bodies](SplitFaceFeature_bodies.md), [StitchFeature.bodies](StitchFeature_bodies.md), [SurfaceDeleteFaceFeature.bodies](SurfaceDeleteFaceFeature_bodies.md), [SweepFeature.bodies](SweepFeature_bodies.md), [TemporaryBRepManager.createFromFile](TemporaryBRepManager_createFromFile.md), [TessellateFeature.bodies](TessellateFeature_bodies.md), [ThickenFeature.bodies](ThickenFeature_bodies.md), [ThreadFeature.bodies](ThreadFeature_bodies.md), [TorusFeature.bodies](TorusFeature_bodies.md), [TrimFeature.bodies](TrimFeature_bodies.md), [UnfoldFeature.bodies](UnfoldFeature_bodies.md), [UnstitchFeature.bodies](UnstitchFeature_bodies.md), [UntrimFeature.bodies](UntrimFeature_bodies.md), [VolumetricCustomFeature.bodies](VolumetricCustomFeature_bodies.md), [VolumetricModelToMeshFeature.bodies](VolumetricModelToMeshFeature_bodies.md), [WebFeature.bodies](WebFeature_bodies.md)

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  

