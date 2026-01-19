# CommandInputs.addStringValueInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new string input to the command.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addStringValueInput(id, name)

# Uses optional arguments.
returnValue = commandInputs_var.addStringValueInput(id, name, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [StringValueCommandInput](StringValueCommandInput.md) | Returns the created StringValueCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| initialValue | string | Specifies the initial value as shown in the dialog. This is an optional argument whose default value is "". |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |

## Version

Introduced in version August 2014  

