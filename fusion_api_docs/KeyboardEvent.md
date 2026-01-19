# KeyboardEvent Object

Derived from: [Event](Event.md) Object  

## Description

An event endpoint that supports the connection to client implemented KeyboardEventHandlers.

## Methods

| Name | Description |
|----|----|
| [add](KeyboardEvent_add.md) | Adds an event handler to this event endpoint. |
| [classType](KeyboardEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](KeyboardEvent_remove.md) | Removes a handler from this event endpoint. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](KeyboardEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](KeyboardEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](KeyboardEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](KeyboardEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Command.keyDown](Command_keyDown.md), [Command.keyUp](Command_keyUp.md)

## Version

Introduced in version August 2014  

