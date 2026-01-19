# ScaleFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing scale features in a component and supports the ability to create new scale features.

## Methods

| Name | Description |
|----|----|
| [add](ScaleFeatures_add.md) | Creates a new scale feature. |
| [classType](ScaleFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ScaleFeatures_createInput.md) | Creates a ScaleFeatureInput object. Use properties and methods on this object to define the scale you want to create and then use the Add method, passing in the ScaleFeatureInput object. |
| [item](ScaleFeatures_item.md) | Function that returns the specified scale feature using an index into the collection. |
| [itemByName](ScaleFeatures_itemByName.md) | Function that returns the specified scale feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ScaleFeatures_count.md) | The number of scale features in the collection. |
| [isValid](ScaleFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ScaleFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.scaleFeatures](Features_scaleFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Scale Feature API Sample](ScaleFeatureSample_Sample.md) | Demonstrates creating a new scale feature. |

## Version

Introduced in version January 2015  

