# TessellateFeatures.add Method

Parent Object: [TessellateFeatures](TessellateFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a tessellate feature.

## Syntax

"tessellateFeatures_var" is a variable referencing a [TessellateFeatures](TessellateFeatures.md) object.

```python
returnValue = tessellateFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [TessellateFeature](TessellateFeature.md) | Returns the newly created TessellateFeatureInput object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [TessellateFeatureInput](TessellateFeatureInput.md) | A TessellateFeatureInput object that defines the desired tessellate feature. Use the createInput method to create a new TessellateFeatureInput object and then use methods on it (the TessellateFeatureInput object) to define the tessellate. |

## Version

Introduced in version January 2025  

