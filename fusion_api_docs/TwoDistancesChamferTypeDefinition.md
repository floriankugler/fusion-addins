# TwoDistancesChamferTypeDefinition Object

Derived from: [ChamferTypeDefinition](ChamferTypeDefinition.md) Object  

## Description

This object is retired. See more information in the 'Remarks' section below.  

Provides information to create a chamfer that is defined by a two distances from the edge.

## Methods

| Name | Description |
|----|----|
| [classType](TwoDistancesChamferTypeDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [distanceOne](TwoDistancesChamferTypeDefinition_distanceOne.md) | Returns the parameter controlling the first distance. You can edit the distance by editing the value of the parameter object. |
| [distanceTwo](TwoDistancesChamferTypeDefinition_distanceTwo.md) | Returns the parameter controlling the second distance. You can edit the distance by editing the value of the parameter object. |
| [isValid](TwoDistancesChamferTypeDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TwoDistancesChamferTypeDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](TwoDistancesChamferTypeDefinition_parentFeature.md) | Returns the feature that owns this chamfer type definition |

## Version

Introduced in version November 2014  

