# JointList.item Method

Parent Object: [JointList](JointList.md)  

## Description

Function that returns the specified joint using an index into the list.

## Syntax

"jointList_var" is a variable referencing a [JointList](JointList.md) object.

```python
returnValue = jointList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the list to return. The first item in the list has an index of 0. |

## Version

Introduced in version January 2016  

