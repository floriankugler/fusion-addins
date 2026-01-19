# MeshRepairFeatureInput.density Property

Parent Object: [MeshRepairFeatureInput](MeshRepairFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Controls the density of the newly created triangles in RebuildMeshRepairType, default value is 128. The values can range between 8 and 256. Only valid if meshRepairType is RebuildMeshRepairType.

## Syntax

"meshRepairFeatureInput_var" is a variable referencing a MeshRepairFeatureInput object.  

```python
# Get the value of the property.
propertyValue = meshRepairFeatureInput_var.density

# Set the value of the property.
meshRepairFeatureInput_var.density = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version March 2024  

