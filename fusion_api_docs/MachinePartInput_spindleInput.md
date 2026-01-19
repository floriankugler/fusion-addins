# MachinePartInput.spindleInput Property

Parent Object: [MachinePartInput](MachinePartInput.md)  

## Description

Gets or sets an spindle input object to create a new MachineSpindle with this part. Only valid when partType is not Axis.

## Syntax

"machinePartInput_var" is a variable referencing a MachinePartInput object.  

```python
# Get the value of the property.
propertyValue = machinePartInput_var.spindleInput

# Set the value of the property.
machinePartInput_var.spindleInput = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachineSpindleInput](MachineSpindleInput.md).

## Version

Introduced in version April 2023  

