# OffsetConstraintInput.offset Property

Parent Object: [OffsetConstraintInput](OffsetConstraintInput.md)  

## Description

Gets and sets the value that defines the offset. This is a ValueInput object so it can be a float value to define the offset in centimeters or it can be a string defining an expression that will be used by the parameter controlling the offset. A positive offset value creates the offset curve to the "right" and a negative offset value goes to the "left".  

The flow direction of the provided curves implies the offset direction. For example, if two connected lines are offset, the flow direction is from line 1 to line 2. Left and right are evaluated relative to the input geometry. If you are standing on line 1 and looking towards line 2, the offset's left side is on your left, and the right side is to your right. Closed single curves like circles and ellipses always have a counterclockwise flow, so a positive offset is always to the outside. For closed splines, the positive direction is based on the spline's parameterization.

## Syntax

"offsetConstraintInput_var" is a variable referencing an OffsetConstraintInput object.  

```python
# Get the value of the property.
propertyValue = offsetConstraintInput_var.offset

# Set the value of the property.
offsetConstraintInput_var.offset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version September 2024  

