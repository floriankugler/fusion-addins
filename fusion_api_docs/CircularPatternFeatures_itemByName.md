# CircularPatternFeatures.itemByName Method

Parent Object: [CircularPatternFeatures](CircularPatternFeatures.md)  

## Description

Function that returns the specified circular pattern feature using the name of the feature.

## Syntax

"circularPatternFeatures_var" is a variable referencing a [CircularPatternFeatures](CircularPatternFeatures.md) object.

```python
returnValue = circularPatternFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternFeature](CircularPatternFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

