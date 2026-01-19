# SilhouetteSplitFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a silhouette split feature.

## Methods

| Name | Description |
|----|----|
| [classType](SilhouetteSplitFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](SilhouetteSplitFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SilhouetteSplitFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](SilhouetteSplitFeatureInput_operation.md) | Gets and sets the type of silhouette split operation to perform. |
| [targetBaseFeature](SilhouetteSplitFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [targetBody](SilhouetteSplitFeatureInput_targetBody.md) | Gets and sets the solid body to split. |
| [viewDirection](SilhouetteSplitFeatureInput_viewDirection.md) | Gets and sets the entity that defines the silhouette view direction, which can be a construction axis, linear BRepEdge, planar BRepFace or a construction plane. |

## Accessed From

[SilhouetteSplitFeatures.createInput](SilhouetteSplitFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Silhouette Split Feature API Sample](SilhouetteSplitFeatureSample_Sample.md) | Demonstrates creating a new silhouette split feature. |

## Version

Introduced in version June 2015  

