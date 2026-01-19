# MouseEvent Object

Derived from: [Event](Event.md) Object  

## Description

An event endpoint that supports the connection to client implemented MouseEventHandlers.

## Methods

| Name | Description |
|----|----|
| [add](MouseEvent_add.md) | Adds an event handler to this event endpoint. |
| [classType](MouseEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](MouseEvent_remove.md) | Removes a handler from this event endpoint. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MouseEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](MouseEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](MouseEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](MouseEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Command.mouseClick](Command_mouseClick.md), [Command.mouseDoubleClick](Command_mouseDoubleClick.md), [Command.mouseDown](Command_mouseDown.md), [Command.mouseDrag](Command_mouseDrag.md), [Command.mouseDragBegin](Command_mouseDragBegin.md), [Command.mouseDragEnd](Command_mouseDragEnd.md), [Command.mouseMove](Command_mouseMove.md), [Command.mouseUp](Command_mouseUp.md), [Command.mouseWheel](Command_mouseWheel.md)

## Version

Introduced in version August 2014  

