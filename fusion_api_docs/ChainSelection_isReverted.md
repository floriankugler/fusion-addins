# ChainSelection.isReverted Property

Parent Object: [ChainSelection](ChainSelection.md)  

## Description

Property to control if the curve is reverted or not. The curve needs to be reverted, if Fusion's guess does not match the user's expectation.  

The initial tool placement depends on the first input edge or sketch line and the height of the bordering faces or sketch boundaries, with the tool being placed outside of the higher face or sketch boundary.

## Syntax

"chainSelection_var" is a variable referencing a ChainSelection object.  

```python
# Get the value of the property.
propertyValue = chainSelection_var.isReverted

# Set the value of the property.
chainSelection_var.isReverted = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version April 2023  

