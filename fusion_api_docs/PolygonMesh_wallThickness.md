# PolygonMesh.wallThickness Property

Parent Object: [PolygonMesh](PolygonMesh.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the wall thickness per node in cm. This property calculates the wall thickness of the mesh, i.e. the distance of a surface of the mesh to the opposing surface.

## Syntax

"polygonMesh_var" is a variable referencing a PolygonMesh object.  

```python
# Get the value of the property.
propertyValue = polygonMesh_var.wallThickness
```

## Property Value

This is a read only property whose value is an array of type float.

## Version

Introduced in version May 2025  

