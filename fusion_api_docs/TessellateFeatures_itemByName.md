# TessellateFeatures.itemByName Method

Parent Object: [TessellateFeatures](TessellateFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Function that returns the specified Tessellate feature using the name of the feature.

## Syntax

"tessellateFeatures_var" is a variable referencing a [TessellateFeatures](TessellateFeatures.md) object.

```python
returnValue = tessellateFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [TessellateFeature](TessellateFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version January 2025  

