# GeometryGraphNodeProperty.beamNetwork Property

Parent Object: [GeometryGraphNodeProperty](GeometryGraphNodeProperty.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Set the value of the property. The value should be a BeamNetwork object, which defines the geometry by defining vertices, beams and radii of the beams.

## Syntax

"geometryGraphNodeProperty_var" is a variable referencing a GeometryGraphNodeProperty object.  

```python
# Get the value of the property.
propertyValue = geometryGraphNodeProperty_var.beamNetwork

# Set the value of the property.
geometryGraphNodeProperty_var.beamNetwork = propertyValue
```

## Property Value

This is a read/write property whose value is a [BeamNetwork](BeamNetwork.md).

## Version

Introduced in version July 2025  

