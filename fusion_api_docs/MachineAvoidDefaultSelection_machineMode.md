# MachineAvoidDefaultSelection.machineMode Property

Parent Object: [MachineAvoidDefaultSelection](MachineAvoidDefaultSelection.md)  

## Description

Desired machining mode. The default is Avoid. The current machining mode will determine which value the radial and axial offset functions refer to. When set to Machine, the radial and axial offset methods will read/set the stock to leave parameter. When set to Avoid, the radial and axial offset methods will read/set the clearance value, and the Fixture mode will map to the relative fixture clearance value.

## Syntax

"machineAvoidDefaultSelection_var" is a variable referencing a MachineAvoidDefaultSelection object.  

```python
# Get the value of the property.
propertyValue = machineAvoidDefaultSelection_var.machineMode

# Set the value of the property.
machineAvoidDefaultSelection_var.machineMode = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachiningMode](MachiningMode.md).

## Version

Introduced in version September 2024  

