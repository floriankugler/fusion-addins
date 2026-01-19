# RuledSurfaceFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Ruled Surface features in a component and supports the ability to create new Ruled Surface features.

## Methods

| Name | Description |
|----|----|
| [add](RuledSurfaceFeatures_add.md) | Creates a new RuledSurface feature. |
| [classType](RuledSurfaceFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](RuledSurfaceFeatures_createInput.md) | Creates a RuledSurfaceFeatureInput object that defines the input needed to create a ruled surface feature. Use the input object to define the input to create the desired feature and then use the Add method, passing in the RuledSurfaceFeatureInput object. |
| [item](RuledSurfaceFeatures_item.md) | Function that returns the specified ruled surface feature using an index into the collection. |
| [itemByName](RuledSurfaceFeatures_itemByName.md) | Function that returns the specified RuledSurface feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RuledSurfaceFeatures_count.md) | The number of RuledSurface features in the collection. |
| [isValid](RuledSurfaceFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RuledSurfaceFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.ruledSurfaceFeatures](Features_ruledSurfaceFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Ruled Surface Feature API Sample](RuledSurfaceFeatureSample_Sample.md) | Demonstrates creating a new ruled surface feature. |

## Version

Introduced in version September 2020  

