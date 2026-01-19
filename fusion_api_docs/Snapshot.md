# Snapshot Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a Snapshot in the timeline

## Methods

| Name | Description |
|----|----|
| [classType](Snapshot_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](Snapshot_deleteMe.md) | Deletes this snapshot. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Snapshot_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](Snapshot_name.md) | Gets and sets the name of the snapshot as seen in the timeline. |
| [objectType](Snapshot_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [timelineObject](Snapshot_timelineObject.md) | Returns the timeline object associated with this snapshot. |

## Accessed From

[Snapshots.add](Snapshots_add.md), [Snapshots.item](Snapshots_item.md)

## Version

Introduced in version August 2014  

