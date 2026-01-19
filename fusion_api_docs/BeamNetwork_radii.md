# BeamNetwork.radii Property

Parent Object: [BeamNetwork](BeamNetwork.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The radii of the beams. Each radius is a double value. The radii define the radius of one end of the beam that corresponds to the same index in the beams array. The size of the array should be a multiple of 2, and equal to the length of the beams array.

## Syntax

"beamNetwork_var" is a variable referencing a BeamNetwork object.  

```python
# Get the value of the property.
propertyValue = beamNetwork_var.radii

# Set the value of the property.
beamNetwork_var.radii = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type double.

## Version

Introduced in version July 2025  

