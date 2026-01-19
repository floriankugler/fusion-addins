# ConstructionAxisEdgeDefinition Object

Derived from: [ConstructionAxisDefinition](ConstructionAxisDefinition.md) Object  

## Description

The definition for a parametric construction axis created using the SetbyEdge method

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionAxisEdgeDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [edgeEntity](ConstructionAxisEdgeDefinition_edgeEntity.md) | Gets and sets the linear edge, construction line, or sketch line that defines the construction axis. |
| [isValid](ConstructionAxisEdgeDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionAxisEdgeDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentConstructionAxis](ConstructionAxisEdgeDefinition_parentConstructionAxis.md) | Returns the ConstructionAxis object |

## Version

Introduced in version August 2014  

