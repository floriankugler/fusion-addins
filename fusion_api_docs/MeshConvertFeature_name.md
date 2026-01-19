# MeshConvertFeature.name Property

Parent Object: [MeshConvertFeature](MeshConvertFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the name of the feature as seen in the browser (non-parametric) or in the timeline (parametric).

## Syntax

"meshConvertFeature_var" is a variable referencing a MeshConvertFeature object.  

```python
# Get the value of the property.
propertyValue = meshConvertFeature_var.name

# Set the value of the property.
meshConvertFeature_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version July 2025  

