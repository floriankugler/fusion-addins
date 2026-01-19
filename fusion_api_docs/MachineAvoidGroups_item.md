# MachineAvoidGroups.item Method

Parent Object: [MachineAvoidGroups](MachineAvoidGroups.md)  

## Description

Function that returns the specified machine/avoid group selection object using an index into the collection.

## Syntax

"machineAvoidGroups_var" is a variable referencing a [MachineAvoidGroups](MachineAvoidGroups.md) object.

```python
returnValue = machineAvoidGroups_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2024  

