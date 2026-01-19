# BeamNetwork.vertices Property

Parent Object: [BeamNetwork](BeamNetwork.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The vertices of the beam network. Each vertex is a Point3D.

## Syntax

"beamNetwork_var" is a variable referencing a BeamNetwork object.  

```python
# Get the value of the property.
propertyValue = beamNetwork_var.vertices

# Set the value of the property.
beamNetwork_var.vertices = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Point3D](Point3D.md).

## Version

Introduced in version July 2025  

