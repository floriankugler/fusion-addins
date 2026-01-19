# MergeFacesFeatures Object

Derived from: [Base](Base.md) Object  

## Description

A collection object that supports the ability to merge faces. Merging faces is currently limited to a Direct Modeling design or a body in a base feature. The result of merging faces is a direct B-Rep modification, and the change is not represented as a feature in the browser. As a result, a MergeFacesFeature object does not exist, and this collection only supports the merging faces and not accessing any existing features.

## Methods

| Name | Description |
|----|----|
| [add](MergeFacesFeatures_add.md) | Creates a new merge face feature. |
| [classType](MergeFacesFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](MergeFacesFeatures_createInput.md) | Creates a MergeFacesFeatureInput object for defining a simple merge face feature. Use properties and methods on this object to define the merge you want to create and then use the Add method, passing in the MergeFacesFeatureInput object. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MergeFacesFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MergeFacesFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.mergeFacesFeatures](Features_mergeFacesFeatures.md)

## Version

Introduced in version September 2024  

