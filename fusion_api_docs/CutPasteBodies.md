# CutPasteBodies Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing cut-paste features in a design. These are created in the UI by cutting and then pasting a B-Rep body.

## Methods

| Name | Description |
|----|----|
| [add](CutPasteBodies_add.md) | Cuts and copies the specified body into the component that owns this CutPasteBodies collection. This is effectively the equivalent of moving a body. |
| [classType](CutPasteBodies_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CutPasteBodies_item.md) | Function that returns the specified Cut/Paste Body feature using an index into the collection. |
| [itemByName](CutPasteBodies_itemByName.md) | Function that returns the specified Cut/Paste Body feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](CutPasteBodies_count.md) | The number of Cut/Paste Body features in the collection. |
| [isValid](CutPasteBodies_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CutPasteBodies_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.cutPasteBodies](Features_cutPasteBodies.md)

## Samples

| Name | Description |
|----|----|
| [Cut Paste Bodies API Sample](CutPasteBodiesSample_Sample.md) | Demonstrates how to use Cut Paste Bodies related API. |

## Version

Introduced in version June 2017  

