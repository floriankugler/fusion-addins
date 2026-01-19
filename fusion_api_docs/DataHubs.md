# DataHubs Object

Derived from: [Base](Base.md) Object  

## Description

Collection object that provides a list of all available hubs.

## Methods

| Name | Description |
|----|----|
| [asArray](DataHubs_asArray.md) | Get the current list of all hubs. |
| [classType](DataHubs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DataHubs_item.md) | Returns the specified hub. |
| [itemById](DataHubs_itemById.md) | Returns the hub specified using the ID of the hub. |

## Properties

| Name | Description |
| --- | --- |
| [count](DataHubs_count.md) | The number of hubs in this collection. |
| [isValid](DataHubs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataHubs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Data.dataHubs](Data_dataHubs.md)

## Version

Introduced in version September 2016  

