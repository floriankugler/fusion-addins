# ApplicationCommandEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing ApplicationCommandEvent to an ApplicationCommandEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](ApplicationCommandEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [commandDefinition](ApplicationCommandEventArgs_commandDefinition.md) | Returns the CommandDefinition object for the command the event is being fired for. |
| [commandId](ApplicationCommandEventArgs_commandId.md) | Returns the unique id of the command the event if being fired for. |
| [firingEvent](ApplicationCommandEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isCanceled](ApplicationCommandEventArgs_isCanceled.md) | Used during the commandStarting event to get or set if the command should be allowed to continue executing or be canceled. This defaults to false, which will allow the command to execute. Setting this to true will cancel the command and not begin the execution. This property should be ignored for all events besides the commandStarting event. |
| [isValid](ApplicationCommandEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ApplicationCommandEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [terminationReason](ApplicationCommandEventArgs_terminationReason.md) | Returns the reason the command is being terminated. This property should be ignored for all events besides the commandTerminated event. |

## Version

Introduced in version November 2015  

