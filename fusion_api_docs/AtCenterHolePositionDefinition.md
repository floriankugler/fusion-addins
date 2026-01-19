# AtCenterHolePositionDefinition Object

Derived from: [HolePositionDefinition](HolePositionDefinition.md) Object  

## Description

Provides positioning information for a hole that is positioned at the center of a circular or elliptical edge.

## Methods

| Name | Description |
|----|----|
| [classType](AtCenterHolePositionDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [centerEdge](AtCenterHolePositionDefinition_centerEdge.md) | Returns the circular or elliptical edge the hole is centered at. |
| [isValid](AtCenterHolePositionDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AtCenterHolePositionDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [planarEntity](AtCenterHolePositionDefinition_planarEntity.md) | Returns the plane that defines the orientation and start of the hole. |

## Version

Introduced in version August 2014  

