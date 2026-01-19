# CommandInputs.addSelectionInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new selection input to the command. This allows you to get entity selections from the user. The default behavior is that only one entity can be selected and it can be of any type. To change the selection behavior to select specific types and control the number of items selected use the methods and properties on the returned SelectionCommandInput object. You can also use the selectionEvent event that's associated with the command to have additional control over the selection process.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addSelectionInput(id, name, commandPrompt)
```

## Return Value

| Type | Description |
|----|----|
| [SelectionCommandInput](SelectionCommandInput.md) | Returns the created SelectionCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| commandPrompt | string | The text in the tooltip shown next to the cursor. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

