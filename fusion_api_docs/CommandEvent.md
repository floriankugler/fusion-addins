# CommandEvent Object

Derived from: [Event](Event.md) Object  

## Description

An event endpoint that supports the connection to client implemented CommandEventHandlers.

## Methods

| Name | Description |
|----|----|
| [add](CommandEvent_add.md) | Adds an event handler object to this event endpoint. |
| [classType](CommandEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](CommandEvent_remove.md) | Removes a handler from this event endpoint. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](CommandEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](CommandEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](CommandEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](CommandEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Command.activate](Command_activate.md), [Command.deactivate](Command_deactivate.md), [Command.destroy](Command_destroy.md), [Command.execute](Command_execute.md), [Command.executePreview](Command_executePreview.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

