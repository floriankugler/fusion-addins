# DeleteFaceFeatures.item Method

Parent Object: [DeleteFaceFeatures](DeleteFaceFeatures.md)  

## Description

Function that returns the specified DeleteFaceFeature object using an index into the collection.

## Syntax

"deleteFaceFeatures_var" is a variable referencing a [DeleteFaceFeatures](DeleteFaceFeatures.md) object.

```python
returnValue = deleteFaceFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DeleteFaceFeature](DeleteFaceFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2016  

