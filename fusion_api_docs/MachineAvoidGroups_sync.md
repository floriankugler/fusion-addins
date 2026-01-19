# MachineAvoidGroups.sync Method

Parent Object: [MachineAvoidGroups](MachineAvoidGroups.md)  

## Description

Function that synchronizes the selections and properties of the default groups from the current operation. This is needed when there are changes made to parameters that drive the default groups (e.g. Setup model or fixture selection changes to be reflected in the MachineAvoidGroups object on the API side). WARNING: This function must not be called before applyMachineAvoidGroups, because temporary group settings and selections will not have been stored in the operation object and will be overwritten.

## Syntax

"machineAvoidGroups_var" is a variable referencing a [MachineAvoidGroups](MachineAvoidGroups.md) object.

```python
returnValue = machineAvoidGroups_var.sync()
```

## Version

Introduced in version September 2024  

