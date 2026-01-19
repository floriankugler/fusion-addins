# MachineAxis.toolChangePosition Property

Parent Object: [MachineAxis](MachineAxis.md)  

## Description

Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. Will return NaN if tool change position isn't set.

## Syntax

"machineAxis_var" is a variable referencing a MachineAxis object.  

```python
# Get the value of the property.
propertyValue = machineAxis_var.toolChangePosition

# Set the value of the property.
machineAxis_var.toolChangePosition = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version July 2025  

