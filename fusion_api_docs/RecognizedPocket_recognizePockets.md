# RecognizedPocket.recognizePockets Method

Parent Object: [RecognizedPocket](RecognizedPocket.md)  

## Description

Gets all recognized pockets from the given body and returns them

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.RecognizedPocket.recognizePockets(body, attackVector)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| body | [Base](Base.md) | Model body on which to recognize pockets |
| attackVector | [Vector3D](Vector3D.md) | A vector defining the orientation in which to search for pockets. This should be the vector pointing down along the tool towards its tip and the pocket floors. |

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version July 2023  

