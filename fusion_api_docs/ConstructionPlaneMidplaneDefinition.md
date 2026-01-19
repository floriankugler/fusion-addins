# ConstructionPlaneMidplaneDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionPlaneMidplaneDefinition defines a ConstructionPlane by...

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneMidplaneDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneMidplaneDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneMidplaneDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneMidplaneDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneMidplaneDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [planarEntityOne](ConstructionPlaneMidplaneDefinition_planarEntityOne.md) | Gets the first planar face or construction plane that defines this ConstructionPlane. |
| [planarEntityTwo](ConstructionPlaneMidplaneDefinition_planarEntityTwo.md) | Gets the second planar face or construction plane that defines this ConstructionPlane. |

## Version

Introduced in version August 2014  

