# RecognizedHoleGroup Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a collection of holes that contain similar geometry. Holes have similar geometry if they contain the same segment types with the same segment heights, diameters, etc...

## Methods

| Name | Description |
|----|----|
| [classType](RecognizedHoleGroup_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RecognizedHoleGroup_item.md) | Returns the hole at the specified index from this hole group. |
| [recognizeHoleGroups](RecognizedHoleGroup_recognizeHoleGroups.md) | \*\*RETIRED\*\* Gets all recognized holes and returns them as hole groupings based on similar geometry. |
| [recognizeHoleGroupsWithInput](RecognizedHoleGroup_recognizeHoleGroupsWithInput.md) | Gets all recognized holes and returns them as hole groupings based on similar geometry. |

## Properties

| Name | Description |
| --- | --- |
| [count](RecognizedHoleGroup_count.md) | Returns the number of holes contained in this hole group. |
| [hasErrors](RecognizedHoleGroup_hasErrors.md) | Returns true if there are any errors associated with this hole group. |
| [hasWarnings](RecognizedHoleGroup_hasWarnings.md) | Returns true if there are any warnings associated with this hole group. |
| [isValid](RecognizedHoleGroup_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RecognizedHoleGroup_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[RecognizedHoleGroups.item](RecognizedHoleGroups_item.md)

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |

## Version

Introduced in version May 2023  

