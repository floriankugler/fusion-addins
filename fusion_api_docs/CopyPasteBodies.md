# CopyPasteBodies Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing copy-paste features in a design. These are created in the UI by copying and then pasting a B-Rep body.

## Methods

| Name | Description |
|----|----|
| [add](CopyPasteBodies_add.md) | Copies the specified body into the component that owns this CopyPasteBodies collection. |
| [classType](CopyPasteBodies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CopyPasteBodies_item.md) | Function that returns the specified Copy/Paste Body feature using an index into the collection. |
| [itemByName](CopyPasteBodies_itemByName.md) | Function that returns the specified Copy/Paste Body feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](CopyPasteBodies_count.md) | The number of Copy/Paste Body features in the collection. |
| [isValid](CopyPasteBodies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CopyPasteBodies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.copyPasteBodies](Features_copyPasteBodies.md)

## Samples

| Name | Description |
|----|----|
| [Copy Paste Bodies API Sample](CopyPasteBodiesSample_Sample.md) | Demonstrates how to use Copy Paste Bodies related API. |

## Version

Introduced in version June 2017  

