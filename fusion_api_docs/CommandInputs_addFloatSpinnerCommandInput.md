# CommandInputs.addFloatSpinnerCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new spinner input to the command. The value type is float.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addFloatSpinnerCommandInput(id, name, unitType, min, max, spinStep, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [FloatSpinnerCommandInput](FloatSpinnerCommandInput.md) | Returns the created FloatSpinnerCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| unitType | string | The unit type of the value. This will be used to validate the input and the returned Value object will be of this type. |
| min | double | Provides the minimum value in database units. |
| max | double | Provides the maximum value in database units. |
| spinStep | double | Sets the spin step value in the unit type set by the unitType argument. The value should be more than zero. This is the amount the slider will advance when the user clicks the spin button beside the value. |
| initialValue | double | The initial value of this input as shown in the dialog. This value is assumed to be in database units for the specified unit type |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

