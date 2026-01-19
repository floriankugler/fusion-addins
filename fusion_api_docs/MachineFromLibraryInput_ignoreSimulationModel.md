# MachineFromLibraryInput.ignoreSimulationModel Property

Parent Object: [MachineFromLibraryInput](MachineFromLibraryInput.md)  

## Description

Gets and sets whether or not to ignore the simulation model when creating or loading the machine. If set to true the simulation model will not be set on the new machine.

## Remarks

This can be useful if you don't have write access to the simulation machine. This can be the case if:  

- The simulation machine is not in your local library.  

- The simulation machine is not saved in your hub.  

- You don't have write access to the hub or location where it was saved.

## Syntax

"machineFromLibraryInput_var" is a variable referencing a MachineFromLibraryInput object.  

```python
# Get the value of the property.
propertyValue = machineFromLibraryInput_var.ignoreSimulationModel

# Set the value of the property.
machineFromLibraryInput_var.ignoreSimulationModel = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version April 2023  

