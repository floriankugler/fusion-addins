# ConstructionAxisByLineDefinition Object

Derived from: [ConstructionAxisDefinition](ConstructionAxisDefinition.md) Object  

## Description

The definition for a non-parametric construction axis. In a non-parametric design all construction planes will return this type of definition regardless of how they were initially created.

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionAxisByLineDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [axis](ConstructionAxisByLineDefinition_axis.md) | Gets and sets the infinite line that defines the position and direction of the axis |
| [isValid](ConstructionAxisByLineDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionAxisByLineDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionAxis](ConstructionAxisByLineDefinition_parentConstructionAxis.md) | Returns the ConstructionAxis object |

## Version

Introduced in version August 2014  

