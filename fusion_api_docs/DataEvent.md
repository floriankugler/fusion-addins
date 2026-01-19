# DataEvent Object

Derived from: [Event](Event.md) Object  

## Description

A Data event is an event associated with operations on Data items.

## Methods

| Name | Description |
|----|----|
| [add](DataEvent_add.md) | Add a handler to be notified when the data event occurs. |
| [classType](DataEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](DataEvent_remove.md) | Removes a handler from the event. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](DataEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](DataEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](DataEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](DataEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Application.dataFileComplete](Application_dataFileComplete.md), [Application.dataFileCopyComplete](Application_dataFileCopyComplete.md)

## Version

Introduced in version January 2022  

