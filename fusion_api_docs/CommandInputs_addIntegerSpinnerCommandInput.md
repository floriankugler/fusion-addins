# CommandInputs.addIntegerSpinnerCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new spinner input to the command. The value type is integer.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addIntegerSpinnerCommandInput(id, name, min, max, spinStep, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [IntegerSpinnerCommandInput](IntegerSpinnerCommandInput.md) | Returns the created IntegerSpinnerCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| min | integer | Provides the minimum value. |
| max | integer | Provides the maximum value. |
| spinStep | uinteger | Provides the spin step. The value should be more than zero. This is the amount the slider will advance when the user clicks the spin button beside the value. |
| initialValue | integer | The initial value of this input as shown in the dialog. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

