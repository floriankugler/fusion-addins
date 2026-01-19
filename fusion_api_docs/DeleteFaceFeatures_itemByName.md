# DeleteFaceFeatures.itemByName Method

Parent Object: [DeleteFaceFeatures](DeleteFaceFeatures.md)  

## Description

Function that returns the specified DeleteFaceFeature object using the name of the feature.

## Syntax

"deleteFaceFeatures_var" is a variable referencing a [DeleteFaceFeatures](DeleteFaceFeatures.md) object.

```python
returnValue = deleteFaceFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [DeleteFaceFeature](DeleteFaceFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version August 2016  

