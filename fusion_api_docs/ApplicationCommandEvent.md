# ApplicationCommandEvent Object

Derived from: [Event](Event.md) Object  

## Description

An event endpoint that supports the connection to ApplicationCommandEventHandlers.

## Methods

| Name | Description |
|----|----|
| [add](ApplicationCommandEvent_add.md) | Adds an event handler object to this event endpoint. |
| [classType](ApplicationCommandEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](ApplicationCommandEvent_remove.md) | Removes a handler from this event endpoint. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ApplicationCommandEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ApplicationCommandEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](ApplicationCommandEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](ApplicationCommandEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[UserInterface.commandCreated](UserInterface_commandCreated.md), [UserInterface.commandStarting](UserInterface_commandStarting.md), [UserInterface.commandTerminated](UserInterface_commandTerminated.md)

## Version

Introduced in version November 2015  

