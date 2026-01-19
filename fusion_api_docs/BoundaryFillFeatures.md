# BoundaryFillFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing boundary fill features in a component and supports the ability to create new boundary fill features.

## Methods

| Name | Description |
| --- | --- |
| [add](BoundaryFillFeatures_add.md) | Creates a new boundary fill feature. |
| [classType](BoundaryFillFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](BoundaryFillFeatures_createInput.md) | Creates a BoundaryFillFeatureInput object. Use properties and methods on this object to define the boundary fill you want to create and then use the Add method, passing in the BoundaryFillFeatureInput object. To determine the possible boundaries and allow you to choose which cells to keep, the boundary fill feature does a partial compute when the input object is created. To do this it starts a boundary fill feature transaction and completes the transaction when you call the add method. If you don't call the add method to finish the transaction it leaves Fusion in a bad state and there will be undo problems and possibly a crash. If you have created a BoundFillFeatureInput object and don't want to finish the feature creation, you need to call the cancel method on the BoundaryFillFeatureInput object to safely abort the current boundary fill transaction. |
| [item](BoundaryFillFeatures_item.md) | Function that returns the specified boundary fill feature using an index into the collection. |
| [itemByName](BoundaryFillFeatures_itemByName.md) | Function that returns the specified boundary fill feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](BoundaryFillFeatures_count.md) | The number of boundary fill features in the collection. |
| [isValid](BoundaryFillFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BoundaryFillFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.boundaryFillFeatures](Features_boundaryFillFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |

## Version

Introduced in version June 2015  

