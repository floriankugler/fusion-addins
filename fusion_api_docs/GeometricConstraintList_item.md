# GeometricConstraintList.item Method

Parent Object: [GeometricConstraintList](GeometricConstraintList.md)  

## Description

Function that returns the specified geometry constraint using an index into the collection.

## Syntax

"geometricConstraintList_var" is a variable referencing a [GeometricConstraintList](GeometricConstraintList.md) object.

```python
returnValue = geometricConstraintList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [GeometricConstraint](GeometricConstraint.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

