# GeometricConstraints.createOffsetInput Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates an OffsetConstraintInput object. Use properties and methods on this object to define the offset you want to create and then use the addOffset2 method, passing in the OffsetConstraintInput object, to create the offset.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.createOffsetInput(curves, offset)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetConstraintInput](OffsetConstraintInput.md) | Returns an OffsetConstraintInput object or null in the case of invalid input. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| curves | SketchCurve[] | A set of end connected curves. The Sketch.FindConnectedCurves method is a convenient way to get this set of curves. |
| offset | [ValueInput](ValueInput.md) | The value that defines the offset. This is a ValueInput object so it can be a float value to define the offset in centimeters or it can be a string defining an expression that will be used by the parameter controlling the offset. A positive offset value creates the offset curve to the "right" and a negative offset value goes to the "left". The flow direction of the provided curves implies the offset direction. For example, if two connected lines are offset, the flow direction is from line 1 to line 2. Left and right are evaluated relative to the input geometry. If you are standing on line 1 and looking towards line 2, the offset's left side is on your left, and the right side is to your right. Closed single curves like circles and ellipses always have a counterclockwise flow, so a positive offset is always to the outside. For closed splines, the positive direction is based on the spline's parameterization. |

## Version

Introduced in version September 2024  

