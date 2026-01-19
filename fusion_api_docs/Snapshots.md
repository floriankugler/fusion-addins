# Snapshots Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the Snapshots within a design and provides methods to create new Snapshots.

## Methods

| Name | Description |
|----|----|
| [add](Snapshots_add.md) | Creates a new snapshot. Creating a snapshot is only valid when the HasPendingTransforms property returns true. |
| [classType](Snapshots_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Snapshots_item.md) | Function that returns the specified snapshot in the collection using an index into the collection. |
| [revertPendingSnapshot](Snapshots_revertPendingSnapshot.md) | Reverts and changes that have been made that can be snapshot. This effectively reverts the design back to the last snapshot. This is only valid when the HasPendingSnapshot property returns true. |

## Properties

| Name | Description |
| --- | --- |
| [count](Snapshots_count.md) | The number of items in the collection. |
| [hasPendingSnapshot](Snapshots_hasPendingSnapshot.md) | Indicates if there are any changes that have been made than can be snapshot. |
| [isValid](Snapshots_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Snapshots_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.snapshots](Design_snapshots.md), [FlatPatternProduct.snapshots](FlatPatternProduct_snapshots.md), [WorkingModel.snapshots](WorkingModel_snapshots.md)

## Version

Introduced in version August 2014  

