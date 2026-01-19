# UnstitchFeatures.itemByName Method

Parent Object: [UnstitchFeatures](UnstitchFeatures.md)  

## Description

Function that returns the specified unstitch feature using the name of the feature.

## Syntax

"unstitchFeatures_var" is a variable referencing a [UnstitchFeatures](UnstitchFeatures.md) object.

```python
returnValue = unstitchFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [UnstitchFeature](UnstitchFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

