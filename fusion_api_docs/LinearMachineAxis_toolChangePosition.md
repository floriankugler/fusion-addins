# LinearMachineAxis.toolChangePosition Property

Parent Object: [LinearMachineAxis](LinearMachineAxis.md)  

## Description

Specifies the value that this axis returns to, prior to a tool change. Units are cm for linear axes or radians for rotary axes. Will return NaN if tool change position isn't set.

## Syntax

"linearMachineAxis_var" is a variable referencing a LinearMachineAxis object.  

```python
# Get the value of the property.
propertyValue = linearMachineAxis_var.toolChangePosition

# Set the value of the property.
linearMachineAxis_var.toolChangePosition = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version July 2025  

