# FilletFeatures.itemByName Method

Parent Object: [FilletFeatures](FilletFeatures.md)  

## Description

Function that returns the specified fillet feature using the name of the feature.

## Syntax

"filletFeatures_var" is a variable referencing a [FilletFeatures](FilletFeatures.md) object.

```python
returnValue = filletFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [FilletFeature](FilletFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

