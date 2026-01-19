# CommandEvent.add Method

Parent Object: [CommandEvent](CommandEvent.md)  

## Description

Adds an event handler object to this event endpoint.

## Syntax

"commandEvent_var" is a variable referencing a [CommandEvent](CommandEvent.md) object.

```python
returnValue = commandEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CommandEventHandler](CommandEventHandler.md) | The client implemented CommandEventHandler to be called when this event is triggered. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

