# SweepFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing sweep features in a component and supports the ability to create new sweep features.

## Methods

| Name | Description |
|----|----|
| [add](SweepFeatures_add.md) | Creates a new sweep feature. |
| [classType](SweepFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SweepFeatures_createInput.md) | Creates a SweepFeatureInput object for defining a simple sweep feature with only a path and no guide rail or surface. Use properties and methods on this object to define the sweep you want to create and then use the Add method, passing in the SweepFeatureInput object. |
| [createInputForSolid](SweepFeatures_createInputForSolid.md) | Creates a SweepFeatureInput object for defining a simple sweep feature from a B-Rep solid with a path. Use properties and methods on this object to define the sweep you want to create, and then use the Add method, passing in the SweepFeatureInput object. |
| [item](SweepFeatures_item.md) | Function that returns the specified sweep feature using an index into the collection. |
| [itemByName](SweepFeatures_itemByName.md) | Function that returns the specified sweep feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](SweepFeatures_count.md) | The number of sweep features in the collection. |
| [isValid](SweepFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SweepFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.sweepFeatures](Features_sweepFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Sweep Feature API Sample](SweepFeatureSample_Sample.md) | Demonstrates creating a new sweep feature. |
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |
| [Two Rail Sweep Feature API Sample](TwoRailSweepFeatureSample_Sample.md) | Demonstrates creating new two rail sweep feature. |

## Version

Introduced in version November 2014  

