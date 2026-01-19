# CommandInputs.addGroupCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new Group input to the command. Group Command inputs organize a set of command inputs into a collapsible list within a command dialog.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addGroupCommandInput(id, name)
```

## Return Value

| Type | Description |
|----|----|
| [GroupCommandInput](GroupCommandInput.md) | Returns the created GroupCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this group as seen in the dialog. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

