# OffsetConstraintInput.curves Property

Parent Object: [OffsetConstraintInput](OffsetConstraintInput.md)  

## Description

Gets and sets an array of SketchCurve objects that defines the connected curves that will be offset. The Sketch.FindConnectedCurves method is a convenient way to get this set of curves.

## Syntax

"offsetConstraintInput_var" is a variable referencing an OffsetConstraintInput object.  

```python
# Get the value of the property.
propertyValue = offsetConstraintInput_var.curves

# Set the value of the property.
offsetConstraintInput_var.curves = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [SketchCurve](SketchCurve.md).

## Version

Introduced in version September 2024  

