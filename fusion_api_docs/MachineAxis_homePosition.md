# MachineAxis.homePosition Property

Parent Object: [MachineAxis](MachineAxis.md)  

## Description

Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes. Will return NaN if home position isn't set.

## Syntax

"machineAxis_var" is a variable referencing a MachineAxis object.  

```python
# Get the value of the property.
propertyValue = machineAxis_var.homePosition

# Set the value of the property.
machineAxis_var.homePosition = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  

