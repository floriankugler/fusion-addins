# SketchArcs.addFillet Method

Parent Object: [SketchArcs](SketchArcs.md)  

## Description

Creates a fillet between two sketch entities The side (quadrant) the fillet is created on is determined by the points specified. The point for each entity can be its startSketchPoint or endSketchPoint

## Syntax

"sketchArcs_var" is a variable referencing a [SketchArcs](SketchArcs.md) object.

```python
returnValue = sketchArcs_var.addFillet(firstEntity, firstEntityPoint, secondEnitity, secondEntityPoint, radius)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the newly created SketchArc object (fillet) if the operation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| firstEntity | [SketchCurve](SketchCurve.md) | The first curve for the fillet definition. The curve must be open. |
| firstEntityPoint | [Point3D](Point3D.md) | A point on or closer to one end of the first curve that indicates the side to create the fillet on |
| secondEnitity | [SketchCurve](SketchCurve.md) | The second curve for the fillet definition. The curve must be open. |
| secondEntityPoint | [Point3D](Point3D.md) | A point on or closer to one end of the second curve that indicates the side to create the fillet on |
| radius | double | radius of the arc in centimeters |

## Samples

| Name | Description |
|----|----|
| [Sketch fillet and offset API Sample](SketchFilletAndOffset_Sample.md) | Demonstrates the creation of a fillet in a sketch and offset a set of curves. |

## Version

Introduced in version August 2014  

