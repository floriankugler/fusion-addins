# MachineAvoidSelectionBase.machineMode Property

Parent Object: [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md)  

## Description

Desired machining mode. The default is Avoid. The current machining mode will determine which value the radial and axial offset functions refer to. When set to Machine, the radial and axial offset methods will read/set the stock to leave parameter. When set to Avoid, the radial and axial offset methods will read/set the clearance value, and the Fixture mode will map to the relative fixture clearance value.

## Syntax

"machineAvoidSelectionBase_var" is a variable referencing a MachineAvoidSelectionBase object.  

```python
# Get the value of the property.
propertyValue = machineAvoidSelectionBase_var.machineMode

# Set the value of the property.
machineAvoidSelectionBase_var.machineMode = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachiningMode](MachiningMode.md).

## Version

Introduced in version September 2024  

