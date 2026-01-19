# TessellateFeature.createQuads Property

Parent Object: [TessellateFeature](TessellateFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates quad faces on the mesh body where possible.

## Syntax

"tessellateFeature_var" is a variable referencing a TessellateFeature object.  

```python
# Get the value of the property.
propertyValue = tessellateFeature_var.createQuads

# Set the value of the property.
tessellateFeature_var.createQuads = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

