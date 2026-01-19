# GeometricConstraints.item Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Function that returns the specified sketch constraint using an index into the collection.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.item(index)
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

