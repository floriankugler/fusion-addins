# RotaryMachineAxisConfiguration.wrapAroundAtRange Property

Parent Object: [RotaryMachineAxisConfiguration](RotaryMachineAxisConfiguration.md)  

## Description

Specify the range that the axis value wraps around for unlimited axes. If there are no wrap around limits then wrapAroundAtRange is infinite. Units are radians.

## Syntax

"rotaryMachineAxisConfiguration_var" is a variable referencing a RotaryMachineAxisConfiguration object.  

```python
# Get the value of the property.
propertyValue = rotaryMachineAxisConfiguration_var.wrapAroundAtRange

# Set the value of the property.
rotaryMachineAxisConfiguration_var.wrapAroundAtRange = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachineAxisRange](MachineAxisRange.md).

## Version

Introduced in version April 2023  

