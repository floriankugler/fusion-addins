# PocketRecognitionSelection.minimumPocketDepth Property

Parent Object: [PocketRecognitionSelection](PocketRecognitionSelection.md)  

## Description

The shallowest pocket (measured from top to bottom) to machine.

## Syntax

"pocketRecognitionSelection_var" is a variable referencing a PocketRecognitionSelection object.  

```python
# Get the value of the property.
propertyValue = pocketRecognitionSelection_var.minimumPocketDepth

# Set the value of the property.
pocketRecognitionSelection_var.minimumPocketDepth = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version July 2023  

