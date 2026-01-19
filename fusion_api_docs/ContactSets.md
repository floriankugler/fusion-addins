# ContactSets Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the existing contact sets in a design and supports creating new contact sets.

## Methods

| Name | Description |
|----|----|
| [add](ContactSets_add.md) | Creates a new contact set for the provided occurrences and/or bodies. |
| [classType](ContactSets_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ContactSets_item.md) | Returns the specified contact set using an index into the collection. |
| [itemByName](ContactSets_itemByName.md) | Returns the specified contact set. |

## Properties

| Name | Description |
| --- | --- |
| [count](ContactSets_count.md) | Returns the number of contacts sets in the design. |
| [isValid](ContactSets_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ContactSets_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.contactSets](Design_contactSets.md), [FlatPatternProduct.contactSets](FlatPatternProduct_contactSets.md), [WorkingModel.contactSets](WorkingModel_contactSets.md)

## Samples

| Name | Description |
|----|----|
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version September 2016  

