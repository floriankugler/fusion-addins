# FlangeFeatures.itemByName Method

Parent Object: [FlangeFeatures](FlangeFeatures.md)  

## Description

Function that returns the specified flange feature using the name of the feature.

## Syntax

"flangeFeatures_var" is a variable referencing a [FlangeFeatures](FlangeFeatures.md) object.

```python
returnValue = flangeFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [FlangeFeature](FlangeFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version August 2020  

