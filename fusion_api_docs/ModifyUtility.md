# ModifyUtility Object

Derived from: [Base](Base.md) Object  

## Description

Base class for all modify utilities.

## Methods

| Name | Description |
|----|----|
| [classType](ModifyUtility_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ModifyUtility_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ModifyUtility_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMAdditiveContainer.modifyUtility](CAMAdditiveContainer_modifyUtility.md), [CAMFolder.modifyUtility](CAMFolder_modifyUtility.md), [CAMHoleRecognition.modifyUtility](CAMHoleRecognition_modifyUtility.md), [CAMPattern.modifyUtility](CAMPattern_modifyUtility.md), [NCProgram.modifyUtility](NCProgram_modifyUtility.md), [Operation.modifyUtility](Operation_modifyUtility.md), [OperationBase.modifyUtility](OperationBase_modifyUtility.md), [Setup.modifyUtility](Setup_modifyUtility.md)

## Derived Classes

[AdditiveSetupUtility](AdditiveSetupUtility.md)

## Version

Introduced in version September 2023  

