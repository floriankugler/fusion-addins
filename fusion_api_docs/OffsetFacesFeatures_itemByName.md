# OffsetFacesFeatures.itemByName Method

Parent Object: [OffsetFacesFeatures](OffsetFacesFeatures.md)  

## Description

Function that returns the specified Offset Face feature using the name of the feature. Offset Face features are created in the UI using the "Press Pull" command.

## Syntax

"offsetFacesFeatures_var" is a variable referencing an [OffsetFacesFeatures](OffsetFacesFeatures.md) object.

```python
returnValue = offsetFacesFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFacesFeature](OffsetFacesFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version June 2017  

