# CommandEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing CommandEvent to a CommandEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](CommandEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [command](CommandEventArgs_command.md) | Gets the Command object. |
| [executeFailed](CommandEventArgs_executeFailed.md) | Used during the execute event to get or set that the execute operations failed and the commands transaction should be aborted. This property should be ignored for all events besides the Execute event. |
| [executeFailedMessage](CommandEventArgs_executeFailedMessage.md) | Used during the execute event to get or set a description of an execute failure. This property should be ignored for all events besides the Execute event. |
| [firingEvent](CommandEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](CommandEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isValidResult](CommandEventArgs_isValidResult.md) | Used during the commandStarting event to get or set that the result of preview is valid and the command can reuse the result when OK is hit. This property should be ignored for all events besides the executePreview event. |
| [objectType](CommandEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [terminationReason](CommandEventArgs_terminationReason.md) | Gets the termination reason of the command. It's only valid on the destroy event. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

