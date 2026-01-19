# ArrangeDefinition2DInput.grainDirection Property

Parent Object: [ArrangeDefinition2DInput](ArrangeDefinition2DInput.md)  

## Description

Defines the angle of the grain direction of the envelope. This is only used when the solver type is True Shape. An angle of 0 is in the X direction of the envelope, and the default value is zero.  

This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in radians. If you use a string, it is evaluated the same as a value would be in the command dialog and uses degrees as the units. For example, if you specify "45" it will result in a 45 degree grain direction. Using a string you can also define an equation for the expression, "PartAngle / 2" where "PartAngle"

## Syntax

"arrangeDefinition2DInput_var" is a variable referencing an ArrangeDefinition2DInput object.  

```python
# Get the value of the property.
propertyValue = arrangeDefinition2DInput_var.grainDirection

# Set the value of the property.
arrangeDefinition2DInput_var.grainDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

