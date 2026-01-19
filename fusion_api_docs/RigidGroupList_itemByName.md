# RigidGroupList.itemByName Method

Parent Object: [RigidGroupList](RigidGroupList.md)  

## Description

Function that returns the specified rigid group using a name.

## Syntax

"rigidGroupList_var" is a variable referencing a [RigidGroupList](RigidGroupList.md) object.

```python
returnValue = rigidGroupList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RigidGroup](RigidGroup.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                     |
|------|--------|-------------------------------------------------|
| name | string | The name of the item within the list to return. |

## Version

Introduced in version January 2016  

