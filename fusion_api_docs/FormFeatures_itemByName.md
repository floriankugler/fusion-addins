# FormFeatures.itemByName Method

Parent Object: [FormFeatures](FormFeatures.md)  

## Description

Function that returns the specified form feature using the name of the feature.

## Syntax

"formFeatures_var" is a variable referencing a [FormFeatures](FormFeatures.md) object.

```python
returnValue = formFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [FormFeature](FormFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

