# CommandDefinitions.itemById Method

Parent Object: [CommandDefinitions](CommandDefinitions.md)  

## Description

Returns the CommandDefinition that has the specified ID.

## Syntax

"commandDefinitions_var" is a variable referencing a [CommandDefinitions](CommandDefinitions.md) object.

```python
returnValue = commandDefinitions_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [CommandDefinition](CommandDefinition.md) | Returns the CommandDefinition with the specified ID or null if there isn't a command definition with that ID. |

## Parameters

| Name | Type   | Description                                 |
|------|--------|---------------------------------------------|
| id   | string | The ID of the command definition to return. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Custom Event Sample](CustomEventSample_Sample.md) | Demonstrates the ability to call into the main thread from a worker thread. This sample is an add-in. To use it, use the Scripts and Add-Ins command to create a new add-in. Delete all of the code in the newly created add-in and replace it with the code below. Have a model open that has a parameter named "Length". Load the add-in. The add-in will change the value of the parameter every two seconds using a random value between 1 and 10. |

## Version

Introduced in version August 2014  

