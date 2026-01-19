# MachineFromFileInput.ignoreSimulationModel Property

Parent Object: [MachineFromFileInput](MachineFromFileInput.md)  

## Description

Whether or not to ignore the simulation model when creating/loading the machine. If set to true the simulation model will not be set on the new machine.

## Remarks

This can be useful if you don't have write access to the simulation machine. This can be the case if:  

- The simulation machine is not in your local library.  

- The simulation machine is not saved in your hub.  

- You don't have write access to the hub or location where it was saved.

## Syntax

"machineFromFileInput_var" is a variable referencing a MachineFromFileInput object.  

```python
# Get the value of the property.
propertyValue = machineFromFileInput_var.ignoreSimulationModel

# Set the value of the property.
machineFromFileInput_var.ignoreSimulationModel = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version April 2023  

