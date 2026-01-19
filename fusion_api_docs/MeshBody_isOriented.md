# MeshBody.isOriented Property

Parent Object: [MeshBody](MeshBody.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Check to see if the mesh is oriented - i.e. every edge has at most two triangles, and those triangles have consistent orientations. Returns true if the mesh is oriented, false if not.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.isOriented
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2024  

