# RecognizedHole.segment Method

Parent Object: [RecognizedHole](RecognizedHole.md)  

## Description

Returns the segment at the specified index from this hole. The collection of segments that comprise this hole are in order. The first segment is at the top of this hole and the last segment is at the bottom.

## Syntax

"recognizedHole_var" is a variable referencing a [RecognizedHole](RecognizedHole.md) object.

```python
returnValue = recognizedHole_var.segment(index)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the segment within this hole to return. The first segment in this hole has an index of 0. |

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version May 2023  

