# HoleFeature.setPositionBySketchPoints Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Redefines the position and orientation of the hole using a set of points.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setPositionBySketchPoints(sketchPoints)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchPoints | [ObjectCollection](ObjectCollection.md) | A collection of sketch points that defines the positions of the holes. The orientation is inferred from the normal of the point's parent sketch. The natural direction will be opposite the normal of the sketch. All of the points must be in the same sketch. |

## Version

Introduced in version June 2015  

