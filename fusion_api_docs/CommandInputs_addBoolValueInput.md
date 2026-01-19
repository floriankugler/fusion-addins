# CommandInputs.addBoolValueInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new boolean input to the command. The input can be shown as a check box or a button. If it's a button you need to specify the resource folder to define the icon to use. Buttons don't have an up or down state but can just be clicked.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addBoolValueInput(id, name, isCheckBox)

# Uses optional arguments.
returnValue = commandInputs_var.addBoolValueInput(id, name, isCheckBox, resourceFolder, initialValue)
```

## Return Value

| Type | Description |
|----|----|
| [BoolValueCommandInput](BoolValueCommandInput.md) | Returns the created BoolValueCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| isCheckBox | boolean | Specifies if this input should be displayed as a check box or a button. If true a check box is displayed, if false a button is displayed that can be clicked to toggle it's state. |
| resourceFolder | string | Specifies the folder that contains the icon for the input. This is optional if isCheckBox is true. If it's defined for a check box, the check box will display as a button using the icon and will have an up or down state. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument whose default value is "". |
| initialValue | boolean | Specifies the initial value of the check box or button where for a check box the value of True results in it being checked and for a button a value of true results in the button being pressed. This is an optional argument whose default value is False. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

