# PocketSelection.inputGeometry Property

Parent Object: [PocketSelection](PocketSelection.md)  

## Description

Get or set the value of the input geometry. If the value originates from a component instead of an occurrence, or an occurrence outside of the CAM environment, then the subpath is checked against the CAM model tree. For some child classes, this may be the same as the value property, but might also consist of fewer elements. Valid elements depend on the capabilities of the derived class. An exception is thrown if the matching fails or the given entity does not match the expected type.

## Syntax

"pocketSelection_var" is a variable referencing a PocketSelection object.  

```python
# Get the value of the property.
propertyValue = pocketSelection_var.inputGeometry

# Set the value of the property.
pocketSelection_var.inputGeometry = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version April 2023  

