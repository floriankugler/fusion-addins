# RectangularPatternFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing rectangular pattern features in a component and supports the ability to create new rectangular pattern features.

## Methods

| Name | Description |
|----|----|
| [add](RectangularPatternFeatures_add.md) | Creates a new rectangular pattern feature. |
| [classType](RectangularPatternFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](RectangularPatternFeatures_createInput.md) | Creates a RectangularPatternFeatureInput object. Use properties and methods on this object to define the rectangular pattern you want to create and then use the Add method, passing in the RectangularPatternFeatureInput object. |
| [item](RectangularPatternFeatures_item.md) | Function that returns the specified rectangular pattern feature using an index into the collection. |
| [itemByName](RectangularPatternFeatures_itemByName.md) | Function that returns the specified rectangular pattern feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RectangularPatternFeatures_count.md) | The number of rectangular pattern features in the collection. |
| [isValid](RectangularPatternFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RectangularPatternFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.rectangularPatternFeatures](Features_rectangularPatternFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [RectangularPattern Feature](RectangularPatternFeatureSample_Sample.md) | Demonstrates creating a new rectangular pattern feature. |

## Version

Introduced in version November 2014  

