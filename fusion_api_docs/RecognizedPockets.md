# RecognizedPockets Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a collection of pockets.

## Methods

| Name | Description |
|----|----|
| [classType](RecognizedPockets_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RecognizedPockets_item.md) | Returns the pocket at the specified index from this collection of pockets. |

## Properties

| Name | Description |
| --- | --- |
| [count](RecognizedPockets_count.md) | Returns the number of pockets contained in this pocket collection. |
| [isValid](RecognizedPockets_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RecognizedPockets_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RecognizedPocket.recognizePockets](RecognizedPocket_recognizePockets.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version July 2023  

