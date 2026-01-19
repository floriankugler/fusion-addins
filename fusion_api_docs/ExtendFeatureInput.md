# ExtendFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of an extend feature.

## Methods

| Name | Description |
|----|----|
| [classType](ExtendFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [distance](ExtendFeatureInput_distance.md) | Gets and sets the ValueInput object that defines the extend distance |
| [edges](ExtendFeatureInput_edges.md) | Gets and sets the edges to extend |
| [extendAlignment](ExtendFeatureInput_extendAlignment.md) | Gets and sets surface extend alignment to use. |
| [extendType](ExtendFeatureInput_extendType.md) | Gets and sets surface extend type to use |
| [isChainingEnabled](ExtendFeatureInput_isChainingEnabled.md) | Gets and sets if all edges that are tangent or curvature continuous, and end point connected, will be found automatically and extended. |
| [isValid](ExtendFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ExtendFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseFeature](ExtendFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[ExtendFeatures.createInput](ExtendFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Extend Feature API Sample](ExtendFeatureSample_Sample.md) | Demonstrates creating a new extend feature. |

## Version

Introduced in version June 2015  

