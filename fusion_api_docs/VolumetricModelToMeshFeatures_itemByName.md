# VolumetricModelToMeshFeatures.itemByName Method

Parent Object: [VolumetricModelToMeshFeatures](VolumetricModelToMeshFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the item with the specified name.

## Syntax

"volumetricModelToMeshFeatures_var" is a variable referencing a [VolumetricModelToMeshFeatures](VolumetricModelToMeshFeatures.md) object.

```python
returnValue = volumetricModelToMeshFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [VolumetricModelToMeshFeature](VolumetricModelToMeshFeature.md) | Returns the specified item or null in the case where there is no item with the specified name. |

## Parameters

| Name | Type   | Description           |
|------|--------|-----------------------|
| name | string | The name of the item. |

## Version

Introduced in version May 2025  

