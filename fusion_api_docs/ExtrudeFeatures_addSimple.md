# ExtrudeFeatures.addSimple Method

Parent Object: [ExtrudeFeatures](ExtrudeFeatures.md)  

## Description

Creates a basic extrusion that goes from the profile plane the specified distance.

## Syntax

"extrudeFeatures_var" is a variable referencing an [ExtrudeFeatures](ExtrudeFeatures.md) object.

```python
returnValue = extrudeFeatures_var.addSimple(profile, distance, operation)
```

## Return Value

| Type | Description |
|----|----|
| [ExtrudeFeature](ExtrudeFeature.md) | Returns the newly created ExtrudeFeature or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| profile | [Base](Base.md) | The profile argument can be a single Profile, a single planar face, a single SketchText object, or an ObjectCollection consisting of multiple profiles, planar faces, and sketch texts. When an ObjectCollection is used all of the profiles, faces, and sketch texts must be co-planar. This method can only be used to create solid extrusions. To create a surface extrusion you need to use the add method. |
| distance | [ValueInput](ValueInput.md) | ValueInput object that defines the extrude distance. A positive value extrudes in the positive direction of the sketch plane and negative value is in the opposite direction. |
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform. |

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.addSimple](extrudeFeatures_addSimple_Sample.md) | Demonstrates the extrudeFeatures.addSimple method. |
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [ReplaceFace Feature](ReplaceFaceFeatureSample_Sample.md) | Demonstrates creating a new replaceface feature. |
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |

## Version

Introduced in version January 2017  

