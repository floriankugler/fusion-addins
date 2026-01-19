# HoleFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing hole features in a component and supports the ability to create new hole features.

## Methods

| Name | Description |
|----|----|
| [add](HoleFeatures_add.md) | Creates a new hole feature based on the information provided by a HoleFeatureInput object. To create a new hole, use one of the createInput functions to define a new input object for the type of hole you want to create. Use the methods and properties on the input object to define any additional input. Once the information is defined on the input object, you can pass it to the Add method to create the hole. |
| [classType](HoleFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createCounterboreInput](HoleFeatures_createCounterboreInput.md) | Creates a HoleFeatureInput object that defines a counterbore hole. This is not a hole feature but an object used to create a hole feature. Functionality on the returned HoleFeatureInput object is used to define the position and extent of the hole. |
| [createCountersinkInput](HoleFeatures_createCountersinkInput.md) | Creates a HoleFeatureInput object that defines a countersink hole. This is not a hole feature but an object used to create a hole feature. Functionality on the returned HoleFeatureInput object is used to define the position and extent of the hole. |
| [createSimpleInput](HoleFeatures_createSimpleInput.md) | Creates a HoleFeatureInput object that defines a simple hole (a single diameter). This is not a hole feature, but an object used to create a hole feature. Functionality on the returned HoleFeatureInput object is used to define the position and extent of the hole. |
| [item](HoleFeatures_item.md) | Function that returns the specified hole feature using an index into the collection. |
| [itemByName](HoleFeatures_itemByName.md) | Function that returns the specified hole feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](HoleFeatures_count.md) | The number of hole features in the collection. |
| [isValid](HoleFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](HoleFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.holeFeatures](Features_holeFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Hole Feature API Sample](HoleFeatureSample_Sample.md) | Demonstrates creating a new hole feature. |

## Version

Introduced in version August 2014  

