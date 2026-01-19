# MeshConvertFeatureInput.isPreprocessHoles Property

Parent Object: [MeshConvertFeatureInput](MeshConvertFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Smooths the boundaries of open holes in the mesh body. Improves the chance of successful conversion by refining the shape of holes that will remain open. Default value is false. Only valid if meshConvertMethodType is OrganicMeshConvertType.

## Syntax

"meshConvertFeatureInput_var" is a variable referencing a MeshConvertFeatureInput object.  

```python
# Get the value of the property.
propertyValue = meshConvertFeatureInput_var.isPreprocessHoles

# Set the value of the property.
meshConvertFeatureInput_var.isPreprocessHoles = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2025  

