# TangentRelationships.itemByName Method

Parent Object: [TangentRelationships](TangentRelationships.md)  

## Description

Function that returns the specified tangent relationship using a name.

## Syntax

"tangentRelationships_var" is a variable referencing a [TangentRelationships](TangentRelationships.md) object.

```python
returnValue = tangentRelationships_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [TangentRelationship](TangentRelationship.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                           |
|------|--------|-------------------------------------------------------|
| name | string | The name of the item within the collection to return. |

## Version

Introduced in version May 2022  

