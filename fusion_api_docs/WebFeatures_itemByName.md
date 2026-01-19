# WebFeatures.itemByName Method

Parent Object: [WebFeatures](WebFeatures.md)  

## Description

Function that returns the specified web feature using the name of the feature.

## Syntax

"webFeatures_var" is a variable referencing a [WebFeatures](WebFeatures.md) object.

```python
returnValue = webFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [WebFeature](WebFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

