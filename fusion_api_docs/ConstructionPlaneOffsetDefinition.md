# ConstructionPlaneOffsetDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionPlaneOffsetDefinition defines a construction plane that is offset by a specified distance from a planar face or construction plane by a specified distance. A positive or negative value can control the direction of the offset.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneOffsetDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneOffsetDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneOffsetDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneOffsetDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](ConstructionPlaneOffsetDefinition_offset.md) | Returns a Parameter object that controls the value of the offset. You can use properties of the returned Parameter object to modify the offset. |
| [parentConstructionPlane](ConstructionPlaneOffsetDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [planarEntity](ConstructionPlaneOffsetDefinition_planarEntity.md) | Gets the planar face or construction plane this construction plane is parametrically dependent on. |

## Version

Introduced in version August 2014  

