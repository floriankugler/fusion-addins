# ConstructionPlaneThreePointsDefinition Object

Derived from: [ConstructionPlaneDefinition](ConstructionPlaneDefinition.md) Object  

## Description

ConstructionPlaneThreePointDefinition defines a ConstructionPlane by 3 point entities (e.g. (sketch points, vertices or construction points) that form a triangle (i.e. no two points the same and they aren't collinear).

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlaneThreePointsDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [redefine](ConstructionPlaneThreePointsDefinition_redefine.md) | Redefines the input geometry of the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConstructionPlaneThreePointsDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneThreePointsDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionPlane](ConstructionPlaneThreePointsDefinition_parentConstructionPlane.md) | Returns the ConstructionPlane object |
| [pointEntityOne](ConstructionPlaneThreePointsDefinition_pointEntityOne.md) | Gets the first construction point, sketch point or vertex. |
| [pointEntityThree](ConstructionPlaneThreePointsDefinition_pointEntityThree.md) | Gets the third construction point, sketch point or vertex. |
| [pointEntityTwo](ConstructionPlaneThreePointsDefinition_pointEntityTwo.md) | Gets the second construction point, sketch point or vertex. |

## Version

Introduced in version August 2014  

