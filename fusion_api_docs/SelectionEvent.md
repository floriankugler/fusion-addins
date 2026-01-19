# SelectionEvent Object

Derived from: [Event](Event.md) Object  

## Description

An event endpoint that supports the connection to client implemented SelectionEventHandlers.

## Methods

| Name | Description |
|----|----|
| [add](SelectionEvent_add.md) | Adds an event handler to this event endpoint. |
| [classType](SelectionEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](SelectionEvent_remove.md) | Removes a handler from this event endpoint. |

## Properties

| Name | Description |
| --- | --- |
| [activeInput](SelectionEvent_activeInput.md) | Returns the SelectionCommandInput that is currently active in the command dialog and that the user is selecting entities for. This can be used to determine which set of rules you want to apply to determine if the current entity is selectable or not. |
| [isValid](SelectionEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](SelectionEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](SelectionEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](SelectionEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Command.preSelect](Command_preSelect.md), [Command.preSelectEnd](Command_preSelectEnd.md), [Command.preSelectMouseMove](Command_preSelectMouseMove.md), [Command.preSelectStart](Command_preSelectStart.md), [Command.select](Command_select.md), [Command.selectionEvent](Command_selectionEvent.md), [Command.unselect](Command_unselect.md)

## Version

Introduced in version August 2014  

