# MachineAvoidGroups.defaultGroup Method

Parent Object: [MachineAvoidGroups](MachineAvoidGroups.md)  

## Description

Function that returns the specified machine/avoid default group selection object using the group type. Default groups contain surfaces that have a specific meaning within the toolpath operation, for example Model, Fixture, Drive etc.

## Syntax

"machineAvoidGroups_var" is a variable referencing a [MachineAvoidGroups](MachineAvoidGroups.md) object.

```python
returnValue = machineAvoidGroups_var.defaultGroup(type)
```

## Return Value

| Type | Description |
|----|----|
| [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md) | Returns the specified item or null if there isn't a group of the specified type |

## Parameters

| Name | Type | Description |
|----|----|----|
| type | [DefaultGroupType](DefaultGroupType.md) | The type of the default group within the collection to return. There can be only one default group of a given type |

## Version

Introduced in version September 2024  

