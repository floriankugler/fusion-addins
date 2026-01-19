# LoftFeatures.itemByName Method

Parent Object: [LoftFeatures](LoftFeatures.md)  

## Description

Function that returns the specified loft feature using the name of the feature.

## Syntax

"loftFeatures_var" is a variable referencing a [LoftFeatures](LoftFeatures.md) object.

```python
returnValue = loftFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [LoftFeature](LoftFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

