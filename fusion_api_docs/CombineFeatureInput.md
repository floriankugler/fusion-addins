# CombineFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a combine feature.

## Methods

| Name | Description |
|----|----|
| [classType](CombineFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isKeepToolBodies](CombineFeatureInput_isKeepToolBodies.md) | Gets and sets a boolean value for whether or not the tool bodies are retrained after the combine results. The default value is false. |
| [isNewComponent](CombineFeatureInput_isNewComponent.md) | Gets and sets a boolean value for whether or not a new component will be created with the results. The default value is false. In Base feature environment NewComponent does not work. |
| [isValid](CombineFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CombineFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](CombineFeatureInput_operation.md) | Gets and sets the type of operation performed by the combine. The valid values are JoinFeatureOperation, CutFeatureOperation and IntersectFeatureOperation. The default value is JoinFeatureOperation. |
| [targetBaseFeature](CombineFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [targetBody](CombineFeatureInput_targetBody.md) |  |
| [toolBodies](CombineFeatureInput_toolBodies.md) |  |

## Accessed From

[CombineFeatures.createInput](CombineFeatures_createInput.md)

## Version

Introduced in version November 2014  

