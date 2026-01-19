# RecognizedHole Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a hole, a hole is made of one or more segments.

## Methods

| Name | Description |
|----|----|
| [classType](RecognizedHole_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getHoleSignatureXML](RecognizedHole_getHoleSignatureXML.md) | Convert hole signature to XML. The result can be used to create a hole template. |
| [recognizeHoles](RecognizedHole_recognizeHoles.md) | \*\*RETIRED\*\* Returns a collection of all recognized holes. |
| [recognizeHolesWithInput](RecognizedHole_recognizeHolesWithInput.md) | Returns a collection of all recognized holes. |
| [segment](RecognizedHole_segment.md) | Returns the segment at the specified index from this hole. The collection of segments that comprise this hole are in order. The first segment is at the top of this hole and the last segment is at the bottom. |

## Properties

| Name | Description |
| --- | --- |
| [axis](RecognizedHole_axis.md) | Returns the unit vector that points straight up out of the hole in the global coordinate system. |
| [bottom](RecognizedHole_bottom.md) | Returns a point at the center of the hole bottom. |
| [bottomDiameter](RecognizedHole_bottomDiameter.md) | Returns the diameter of the bottom of this hole (bottom diameter of the last segment contained in this hole). |
| [hasErrors](RecognizedHole_hasErrors.md) | Returns true if there are any errors associated with this hole. |
| [hasWarnings](RecognizedHole_hasWarnings.md) | Returns true if there are any warnings associated with this hole. |
| [isThreaded](RecognizedHole_isThreaded.md) | Returns true if at least one segment of this hole is threaded, i.e. associated with a thread feature. |
| [isThrough](RecognizedHole_isThrough.md) | Returns true if this is a through hole, i.e. if the bottom is open. |
| [isValid](RecognizedHole_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RecognizedHole_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [segmentCount](RecognizedHole_segmentCount.md) | Returns the number of segments contained in this hole. |
| [top](RecognizedHole_top.md) | Returns a point at the center of the hole top. |
| [topDiameter](RecognizedHole_topDiameter.md) | Returns the diameter of the top of this hole (top diameter of the first segment contained in this hole). |
| [totalLength](RecognizedHole_totalLength.md) | Returns the total length of all segments contained in this hole. |

## Accessed From

[RecognizedHoleGroup.item](RecognizedHoleGroup_item.md), [RecognizedHoles.item](RecognizedHoles_item.md)

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version May 2023  

