# CommandCreatedEvent.add Method

Parent Object: [CommandCreatedEvent](CommandCreatedEvent.md)  

## Description

Adds an event handler object to this event endpoint.

## Syntax

"commandCreatedEvent_var" is a variable referencing a [CommandCreatedEvent](CommandCreatedEvent.md) object.

```python
returnValue = commandCreatedEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CommandCreatedEventHandler](CommandCreatedEventHandler.md) | The client implemented CommandCreatedEventHandler to be called when this event is triggered. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

