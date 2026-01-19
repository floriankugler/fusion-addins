# CustomEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The ApplicationEventArgs provides information associated with an application event. Note that some properties are not available on every event

## Methods

| Name | Description |
|----|----|
| [classType](CustomEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [additionalInfo](CustomEventArgs_additionalInfo.md) | Information being passed to the add-in in the primary thread from the worker thread or other add-in. |
| [firingEvent](CustomEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](CustomEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Samples

| Name | Description |
|----|----|
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |

## Version

Introduced in version January 2017  

