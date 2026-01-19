# CommandInputs.addValueInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new value input to the command.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addValueInput(id, name, unitType, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [ValueCommandInput](ValueCommandInput.md) | Returns the created ValueCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| unitType | string | The unit type of the value. This will be used to validate the input and the returned Value object will be of this type. |
| initialValue | [ValueInput](ValueInput.md) | The initial value of this input as shown in the dialog. This can be a string or a real. If it's a string it must be able to be evaluated using the specified unit type. If it's a real it is assumed to be in database units for the specified unit type and is displayed as a string |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

