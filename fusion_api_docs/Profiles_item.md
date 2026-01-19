# Profiles.item Method

Parent Object: [Profiles](Profiles.md)  

## Description

Function that returns the specified closed profile using an index into the collection.

## Syntax

"profiles_var" is a variable referencing a [Profiles](Profiles.md) object.

```python
returnValue = profiles_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Profile](Profile.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |

## Version

Introduced in version August 2014  

