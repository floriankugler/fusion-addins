# PathPatternFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing path pattern features in a component and supports the ability to create new path pattern features.

## Methods

| Name | Description |
|----|----|
| [add](PathPatternFeatures_add.md) | Creates a new path pattern feature. |
| [classType](PathPatternFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](PathPatternFeatures_createInput.md) | Creates a PathPatternFeatureInput object. Use properties and methods on this object to define the path pattern you want to create and then use the Add method, passing in the PathPatternFeatureInput object. |
| [item](PathPatternFeatures_item.md) | Function that returns the specified path pattern feature using an index into the collection. |
| [itemByName](PathPatternFeatures_itemByName.md) | Function that returns the specified path pattern feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](PathPatternFeatures_count.md) | The number of path pattern features in the collection. |
| [isValid](PathPatternFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PathPatternFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.pathPatternFeatures](Features_pathPatternFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Path Pattern Feature API Sample](PathPatternFeatureSample_Sample.md) | Demonstrates creating a new path pattern feature. |

## Version

Introduced in version November 2014  

