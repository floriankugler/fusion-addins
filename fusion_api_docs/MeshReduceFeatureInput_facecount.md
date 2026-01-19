# MeshReduceFeatureInput.facecount Property

Parent Object: [MeshReduceFeatureInput](MeshReduceFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the target face count for the reduced mesh as a target for the reduction. Only valid if meshReduceTargetType is FaceCountMeshReduceTargetType.

## Syntax

"meshReduceFeatureInput_var" is a variable referencing a MeshReduceFeatureInput object.  

```python
# Get the value of the property.
propertyValue = meshReduceFeatureInput_var.facecount

# Set the value of the property.
meshReduceFeatureInput_var.facecount = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version March 2024  

