# ThreadFeatures.itemByName Method

Parent Object: [ThreadFeatures](ThreadFeatures.md)  

## Description

Function that returns the specified thread feature using the name of the feature.

## Syntax

"threadFeatures_var" is a variable referencing a [ThreadFeatures](ThreadFeatures.md) object.

```python
returnValue = threadFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ThreadFeature](ThreadFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

