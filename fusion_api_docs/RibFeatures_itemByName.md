# RibFeatures.itemByName Method

Parent Object: [RibFeatures](RibFeatures.md)  

## Description

Function that returns the specified Rib feature using the name of the feature.

## Syntax

"ribFeatures_var" is a variable referencing a [RibFeatures](RibFeatures.md) object.

```python
returnValue = ribFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RibFeature](RibFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

