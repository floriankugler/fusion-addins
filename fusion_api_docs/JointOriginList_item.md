# JointOriginList.item Method

Parent Object: [JointOriginList](JointOriginList.md)  

## Description

Function that returns the specified joint origin using an index into the list.

## Syntax

"jointOriginList_var" is a variable referencing a [JointOriginList](JointOriginList.md) object.

```python
returnValue = jointOriginList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [JointOrigin](JointOrigin.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the list to return. The first item in the list has an index of 0. |

## Version

Introduced in version January 2016  

