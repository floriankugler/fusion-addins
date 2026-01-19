# TangentRelationships.item Method

Parent Object: [TangentRelationships](TangentRelationships.md)  

## Description

Function that returns the specified tangent relationship using an index into the collection.

## Syntax

"tangentRelationships_var" is a variable referencing a [TangentRelationships](TangentRelationships.md) object.

```python
returnValue = tangentRelationships_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [TangentRelationship](TangentRelationship.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version May 2022  

