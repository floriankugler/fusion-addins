# OffsetConstraintInput.dimensionPoint Property

Parent Object: [OffsetConstraintInput](OffsetConstraintInput.md)  

## Description

A location on one of the curves where the offset dimension will be created. A value of null can be used to indicate that a default location should be used.  

When the OffsetContraintInput is created this property defaults to null.

## Syntax

"offsetConstraintInput_var" is a variable referencing an OffsetConstraintInput object.  

```python
# Get the value of the property.
propertyValue = offsetConstraintInput_var.dimensionPoint

# Set the value of the property.
offsetConstraintInput_var.dimensionPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version September 2024  

