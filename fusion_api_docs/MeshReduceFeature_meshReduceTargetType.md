# MeshReduceFeature.meshReduceTargetType Property

Parent Object: [MeshReduceFeature](MeshReduceFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the target criteria for the reduction.

## Syntax

"meshReduceFeature_var" is a variable referencing a MeshReduceFeature object.  

```python
# Get the value of the property.
propertyValue = meshReduceFeature_var.meshReduceTargetType

# Set the value of the property.
meshReduceFeature_var.meshReduceTargetType = propertyValue
```

## Property Value

This is a read/write property whose value is a [MeshReduceTargetTypes](MeshReduceTargetTypes.md).

## Version

Introduced in version March 2024  

