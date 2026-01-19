# Joints.item Method

Parent Object: [Joints](Joints.md)  

## Description

Function that returns the specified joint using an index into the collection.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version July 2015  

