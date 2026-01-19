# RigidGroups.itemByName Method

Parent Object: [RigidGroups](RigidGroups.md)  

## Description

Function that returns the specified rigid group using a name.

## Syntax

"rigidGroups_var" is a variable referencing a [RigidGroups](RigidGroups.md) object.

```python
returnValue = rigidGroups_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RigidGroup](RigidGroup.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| name | string | The name of the item within the collection to return. |

## Version

Introduced in version September 2015  

