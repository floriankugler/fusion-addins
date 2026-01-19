# GeometricConstraints.addTangent Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new tangent constraint between two curves.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addTangent(curveOne, curveTwo)
```

## Return Value

| Type | Description |
|----|----|
| [TangentConstraint](TangentConstraint.md) | Returns the newly created TangentConstraint object or null if the creation failed. |

## Parameters

| Name     | Type                           | Description                     |
|----------|--------------------------------|---------------------------------|
| curveOne | [SketchCurve](SketchCurve.md) | The first curve to be tangent.  |
| curveTwo | [SketchCurve](SketchCurve.md) | The second curve to be tangent. |

## Samples

| Name | Description |
|----|----|
| [Create Circle By 3 Tangents API Sample](CreateCcircleBy3Tangents_Sample.md) | Creates three lines and then draws a circle that is tangent to the lines. It then creates tangent constraints to maintain that relationship. |
| [GeometricConstraints.addTangent](GeometricConstraints_addTangent_Sample.md) | Demonstrates the GeometricConstraints.addTangent method. |
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |

## Version

Introduced in version August 2014  

