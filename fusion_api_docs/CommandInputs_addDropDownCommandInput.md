# CommandInputs.addDropDownCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new empty drop-down input to the command. drop-downs of various types are supported. To add items to the drop down use the returned DropDownCommandInput object.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addDropDownCommandInput(id, name, dropDownStyle)
```

## Return Value

| Type | Description |
|----|----|
| [DropDownCommandInput](DropDownCommandInput.md) | Returns the created DropDownCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this command as seen in the dialog. |
| dropDownStyle | [DropDownStyles](DropDownStyles.md) | Specifies the style of the drop-down. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2015  

