# RectangularPatternFeatures.itemByName Method

Parent Object: [RectangularPatternFeatures](RectangularPatternFeatures.md)  

## Description

Function that returns the specified rectangular pattern feature using the name of the feature.

## Syntax

"rectangularPatternFeatures_var" is a variable referencing a [RectangularPatternFeatures](RectangularPatternFeatures.md) object.

```python
returnValue = rectangularPatternFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternFeature](RectangularPatternFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

