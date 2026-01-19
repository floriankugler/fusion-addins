# TessellateFeatures.createInput Method

Parent Object: [TessellateFeatures](TessellateFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a TessellateFeatureInput object. Use properties and methods on this object to define the tessellation you want to create and then use the add method, passing in the TessellateFeatureInput object.

## Syntax

"tessellateFeatures_var" is a variable referencing a [TessellateFeatures](TessellateFeatures.md) object.

```python
returnValue = tessellateFeatures_var.createInput(bodies)
```

## Return Value

| Type | Description |
|----|----|
| [TessellateFeatureInput](TessellateFeatureInput.md) | Returns the newly created TessellateFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| bodies | BRepBody\[\] | A array with BReb bodies in either a parametric or direct modeling design. |

## Version

Introduced in version January 2025  

