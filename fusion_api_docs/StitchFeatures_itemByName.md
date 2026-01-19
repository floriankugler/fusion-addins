# StitchFeatures.itemByName Method

Parent Object: [StitchFeatures](StitchFeatures.md)  

## Description

Function that returns the specified stitch feature using the name of the feature.

## Syntax

"stitchFeatures_var" is a variable referencing a [StitchFeatures](StitchFeatures.md) object.

```python
returnValue = stitchFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [StitchFeature](StitchFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

