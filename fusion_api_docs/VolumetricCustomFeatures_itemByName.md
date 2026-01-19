# VolumetricCustomFeatures.itemByName Method

Parent Object: [VolumetricCustomFeatures](VolumetricCustomFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the item with the specified internal name.

## Syntax

"volumetricCustomFeatures_var" is a variable referencing a [VolumetricCustomFeatures](VolumetricCustomFeatures.md) object.

```python
returnValue = volumetricCustomFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [VolumetricCustomFeature](VolumetricCustomFeature.md) | Returns the specified item or null in the case where there is no item with the specified name. |

## Parameters

| Name | Type   | Description           |
|------|--------|-----------------------|
| name | string | The name of the item. |

## Version

Introduced in version May 2025  

