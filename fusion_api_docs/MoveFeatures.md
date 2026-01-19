# MoveFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing move features in a component and supports the ability to create new move features.

## Methods

| Name | Description |
|----|----|
| [add](MoveFeatures_add.md) | Creates a new move feature. |
| [classType](MoveFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](MoveFeatures_createInput.md) | \*\*RETIRED\*\* Creates a MoveFeatureInput object. Use properties and methods on this object to define the move feature you want to create and then use the Add method, passing in the MoveFeatureInput object. |
| [createInput2](MoveFeatures_createInput2.md) | Creates a MoveFeatureInput object. Use properties and methods on this object to define how the move is defined and then use the MoveFeatues.add method, passing in the MoveFeatureInput object to create a move feature. |
| [item](MoveFeatures_item.md) | Function that returns the specified move feature using an index into the collection. |
| [itemByName](MoveFeatures_itemByName.md) | Function that returns the specified move feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](MoveFeatures_count.md) | The number of move features in the collection. |
| [isValid](MoveFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MoveFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.moveFeatures](Features_moveFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |

## Version

Introduced in version March 2015  

