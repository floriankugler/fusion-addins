# RecognizedPocket Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a single pocket (an outer boundary with depth and optional islands) which has been recognized on the model. See PocketRecognitionSelection for making a selection as in the UI

## Methods

| Name | Description |
|----|----|
| [classType](RecognizedPocket_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [recognizePockets](RecognizedPocket_recognizePockets.md) | Gets all recognized pockets from the given body and returns them |

## Properties

| Name | Description |
| --- | --- |
| [bottomType](RecognizedPocket_bottomType.md) | Returns the type of bottom edge this pocket has. |
| [boundaries](RecognizedPocket_boundaries.md) | Returns the outside boundaries of this pocket (in cm). |
| [depth](RecognizedPocket_depth.md) | Returns the depth of the pocket in centimeters, i.e. the positive distance from top to bottom |
| [faces](RecognizedPocket_faces.md) | Returns all faces making up the pocket. |
| [isClosed](RecognizedPocket_isClosed.md) | Returns true if this pocket is closed, i.e. if its boundary is a single closed curve. |
| [islands](RecognizedPocket_islands.md) | Returns each island inside this pocket as a separate ProfileLoop object (in cm). |
| [isThrough](RecognizedPocket_isThrough.md) | Returns true if this is a through pocket, i.e. if the bottom is open. |
| [isValid](RecognizedPocket_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RecognizedPocket_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sharedFaces](RecognizedPocket_sharedFaces.md) | Returns all faces making up the pocket, which are shared with other pockets. |

## Accessed From

[RecognizedPockets.item](RecognizedPockets_item.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version July 2023  

