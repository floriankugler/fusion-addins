# CommandInputs.addDistanceValueCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new distance value input to the command. This displays a field in the command dialog where a distance value can be entered. It displays the distance in the dialog using current document default unit. There is also a graphical manipulator associated with the input. You use the setManipulator method of the returned DistanceValueCommandInput object to define the position and orientation of the manipulator.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addDistanceValueCommandInput(id, name, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [DistanceValueCommandInput](DistanceValueCommandInput.md) | Returns the created DistanceValueCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this input as seen in the dialog. If a name is not specified (an empty string), the input will be centered horizontally within it's row in the dialog. If a name is specified it will appear as a left justified label aligned with the other command input labels, and the left side of the image will be aligned with the other command input controls. |
| initialValue | [ValueInput](ValueInput.md) | The initial value of the input. If the value input is a number then it is interpreted as centimeters. If it is a string it uses the units specified in the string or if no units are specified it uses the active units of the design. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

