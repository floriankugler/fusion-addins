# CommandInputs.addAngleValueCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new angle value input to the command. This displays a field in the command dialog where an angle value can be entered. It displays the angle in the dialog using degrees. There is also a graphical manipulator associated with the input to allow the user to graphically set the value. You use the setManipulator method of the returned AngleValueCommandInput object to define the position and orientation of the manipulator.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addAngleValueCommandInput(id, name, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [AngleValueCommandInput](AngleValueCommandInput.md) | Returns the created AngleValueCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this input as seen in the dialog. If a name is not specified (an empty string), the input will be centered horizontally within it's row in the dialog. If a name is specified it will appear as a left justified label aligned with the other command input labels, and the left side of the image will be aligned with the other command input controls. |
| initialValue | [ValueInput](ValueInput.md) | The initial value of the input. If the value input is a number then it is interpreted as radians. If it is a string it uses the units specified in the string or if no units are specified it uses degrees. |

## Version

Introduced in version January 2017  

