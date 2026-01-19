# GeometricConstraints.addSmooth Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new smooth constraint between two curves. One of the curves must be a spline. The other curve can be a spline or any other type of curve.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addSmooth(curveOne, curveTwo)
```

## Return Value

| Type | Description |
|----|----|
| [SmoothConstraint](SmoothConstraint.md) | Returns the newly created SmoothConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curveOne | [SketchCurve](SketchCurve.md) | The first curve to be constrained to be smooth to the second curve. |
| curveTwo | [SketchCurve](SketchCurve.md) | The second curve to be constrained to be smooth to the first curve. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addSmooth](GeometricConstraints_addSmooth_Sample.md) | Demonstrate the GeometricConstraints.addSmooth method. |

## Version

Introduced in version August 2014  

