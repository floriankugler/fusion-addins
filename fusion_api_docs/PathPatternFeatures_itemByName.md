# PathPatternFeatures.itemByName Method

Parent Object: [PathPatternFeatures](PathPatternFeatures.md)  

## Description

Function that returns the specified path pattern feature using the name of the feature.

## Syntax

"pathPatternFeatures_var" is a variable referencing a [PathPatternFeatures](PathPatternFeatures.md) object.

```python
returnValue = pathPatternFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PathPatternFeature](PathPatternFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

