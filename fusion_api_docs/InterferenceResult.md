# InterferenceResult Object

Derived from: [Base](Base.md) Object  

## Description

Represents the interference between bodies and/or occurrences in an interference analysis.

## Methods

| Name | Description |
|----|----|
| [classType](InterferenceResult_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [entityOne](InterferenceResult_entityOne.md) | Returns the first entity involved in the interference |
| [entityTwo](InterferenceResult_entityTwo.md) | Returns the second entity involved in the interference |
| [interferenceBody](InterferenceResult_interferenceBody.md) | Returns a transient BRepBody that represents the volume of interference. |
| [isCreateBody](InterferenceResult_isCreateBody.md) | Gets and sets if this interference volume should be created as a model body. Setting this to true doesn't create the body just indicates that a body is desired. Calling the createBodies method on the interferenceResults object will result in the creation of the model body if this property is true. |
| [isValid](InterferenceResult_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](InterferenceResult_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[InterferenceResults.item](InterferenceResults_item.md)

## Version

Introduced in version November 2015  

