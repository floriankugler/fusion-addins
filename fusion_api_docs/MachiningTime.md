# MachiningTime Object

Derived from: [Base](Base.md) Object  

## Description

Object returned when using the getMachiningTime method from the CAM class. Use the properties on this object to get the machining time results.

## Methods

| Name | Description |
|----|----|
| [classType](MachiningTime_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [feedDistance](MachiningTime_feedDistance.md) | Gets the feed distance in centimeters. |
| [isValid](MachiningTime_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [machiningTime](MachiningTime_machiningTime.md) | Gets the machining time in seconds. |
| [objectType](MachiningTime_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [rapidDistance](MachiningTime_rapidDistance.md) | Gets the calculated rapid distance in centimeters. |
| [toolChangeCount](MachiningTime_toolChangeCount.md) | Gets the number of tool changes. |
| [totalFeedTime](MachiningTime_totalFeedTime.md) | Get the total feed time in seconds. |
| [totalRapidTime](MachiningTime_totalRapidTime.md) | Gets the total rapid feed time in seconds. |
| [totalToolChangeTime](MachiningTime_totalToolChangeTime.md) | Gets the total tool change time in seconds. |

## Accessed From

[CAM.getMachiningTime](CAM_getMachiningTime.md)

## Version

Introduced in version September 2017  

