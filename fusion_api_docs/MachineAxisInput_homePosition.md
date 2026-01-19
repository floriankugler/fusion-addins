# MachineAxisInput.homePosition Property

Parent Object: [MachineAxisInput](MachineAxisInput.md)  

## Description

Specifies the value that this axis returns to when the machine is homed. Units are cm for linear axes or radians for rotary axes.

## Syntax

"machineAxisInput_var" is a variable referencing a MachineAxisInput object.  

```python
# Get the value of the property.
propertyValue = machineAxisInput_var.homePosition

# Set the value of the property.
machineAxisInput_var.homePosition = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  

