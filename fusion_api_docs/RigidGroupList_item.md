# RigidGroupList.item Method

Parent Object: [RigidGroupList](RigidGroupList.md)  

## Description

Function that returns the specified rigid group using an index into the list.

## Syntax

"rigidGroupList_var" is a variable referencing a [RigidGroupList](RigidGroupList.md) object.

```python
returnValue = rigidGroupList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RigidGroup](RigidGroup.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the list to return. The first item in the list has an index of 0. |

## Version

Introduced in version January 2016  

