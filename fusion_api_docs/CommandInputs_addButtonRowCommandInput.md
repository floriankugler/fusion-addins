# CommandInputs.addButtonRowCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new row of buttons as a command input. Depending on the isMultiSelectEnabled argument it can act like an option list where only a single button on the row can be selected at a time or multiple buttons can be selected. The buttons are defined by using the returned ButtonRowCommandInput object.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addButtonRowCommandInput(id, name, isMultiSelectEnabled)
```

## Return Value

| Type | Description |
|----|----|
| [ButtonRowCommandInput](ButtonRowCommandInput.md) | Returns the created ButtonRowCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this command as seen in the dialog. |
| isMultiSelectEnabled | boolean | Sets if this button row can have multiple items selected at once or not. If True, multiple buttons can be selected at once. If False only one button can be selected and selecting another button unselects the one currently selected. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

