# InputChangedEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing InputChangedEvent to a InputEventChangedEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](InputChangedEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](InputChangedEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [input](InputChangedEventArgs_input.md) | Returns the command input that has just changed. |
| [inputs](InputChangedEventArgs_inputs.md) | Returns the collection of command inputs that are associated with the command this event is being fired for. |
| [isValid](InputChangedEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](InputChangedEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

