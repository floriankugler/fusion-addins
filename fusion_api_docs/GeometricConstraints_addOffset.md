# GeometricConstraints.addOffset Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates an offset constraint, which results in creating a new set of curves that are an offset of the input curves. The returned offset constraint provides access to the created curves and the parameter controlling the offset.  

The offset direction is implied by the flow direction of the provided curves. For example, if two connected lines are offset, the flow direction is from line 1 to line 2. A positive offset value creates the offset curve to the "right" of the lines and a negative offset goes to the "left". Left and right are evaluated with respect to the geometry. If you are standing on line 1 looking towards line 2 your left and right are the offset left and right. For closed single curves like circles and ellipses their flow direction is always counterclockwise so a positive offset is always to the outsides.

## Remarks

To access the full capabilities supported by offset, you should use the createOffsetInput and addOffset2 methods.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addOffset(curves, offset, basePoint)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetConstraint](OffsetConstraint.md) | The created OffsetConstraint. You can use properties on the constraint to get information about the offset. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curves | SketchCurve\[\] | A set of end connected curves. The Sketch.FindConnectedCurves method is a convenient way to get this set of curves. |
| offset | [ValueInput](ValueInput.md) | The value that defines the offset. This is a ValueInput object so it can be a float value to define the offset in centimeters or it can be a string defining an expression that will be used by the dimension that controls the offset. |
| basePoint | [Point3D](Point3D.md) | The location on one of the curves where the offset dimension will be created. |

## Version

Introduced in version September 2022  
Retired in version September 2024  

