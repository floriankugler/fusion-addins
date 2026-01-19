# MeshSeparateFeature.isMultipleBodies Property

Parent Object: [MeshSeparateFeature](MeshSeparateFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Separates each face group into an independent mesh body. Only valid if face groups are used as inputs.

## Syntax

"meshSeparateFeature_var" is a variable referencing a MeshSeparateFeature object.  

```python
# Get the value of the property.
propertyValue = meshSeparateFeature_var.isMultipleBodies

# Set the value of the property.
meshSeparateFeature_var.isMultipleBodies = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2025  

