# HoleFeatureInput.setPositionBySketchPoint Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the position and orientation of the hole using a sketch point.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setPositionBySketchPoint(sketchPoint)
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

