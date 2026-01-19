# AsBuiltJointList.item Method

Parent Object: [AsBuiltJointList](AsBuiltJointList.md)  

## Description

Function that returns the specified as-built joint using an index into the list.

## Syntax

"asBuiltJointList_var" is a variable referencing an [AsBuiltJointList](AsBuiltJointList.md) object.

```python
returnValue = asBuiltJointList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJoint](AsBuiltJoint.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the list to return. The first item in the list has an index of 0. |

## Version

Introduced in version January 2016  

