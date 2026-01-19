# HoleFeature.setPositionBySketchPoint Method

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Redefines the position and orientation of the hole using a sketch point.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"holeFeature_var" is a variable referencing a [HoleFeature](HoleFeature.md) object.

```python
returnValue = holeFeature_var.setPositionBySketchPoint(sketchPoint)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchPoint | [SketchPoint](SketchPoint.md) | The sketch point that defines the position of the hole. The orientation is inferred from the normal of the point's parent sketch. The natural direction will be opposite the normal of the sketch. |

## Version

Introduced in version August 2014  

