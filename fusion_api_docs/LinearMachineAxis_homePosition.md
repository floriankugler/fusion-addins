# LinearMachineAxis.homePosition Property

Parent Object: [LinearMachineAxis](LinearMachineAxis.md)  

## Description

Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. Will return NaN if home position isn't set.

## Syntax

"linearMachineAxis_var" is a variable referencing a LinearMachineAxis object.  

```python
# Get the value of the property.
propertyValue = linearMachineAxis_var.homePosition

# Set the value of the property.
linearMachineAxis_var.homePosition = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  

