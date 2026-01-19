# SphereFeatures.item Method

Parent Object: [SphereFeatures](SphereFeatures.md)  

## Description

Function that returns the specified sphere feature using an index into the collection.

## Syntax

"sphereFeatures_var" is a variable referencing a [SphereFeatures](SphereFeatures.md) object.

```python
returnValue = sphereFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SphereFeature](SphereFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

