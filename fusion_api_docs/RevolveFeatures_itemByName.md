# RevolveFeatures.itemByName Method

Parent Object: [RevolveFeatures](RevolveFeatures.md)  

## Description

Function that returns the specified revolve feature using the name of the feature.

## Syntax

"revolveFeatures_var" is a variable referencing a [RevolveFeatures](RevolveFeatures.md) object.

```python
returnValue = revolveFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RevolveFeature](RevolveFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

