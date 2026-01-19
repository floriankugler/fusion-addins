# CommandInputs.addDirectionCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new direction command input to the command. The input can be shown as a check box or a button. If it's a button you need to specify the resource folder to define the icon to use for the Button.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addDirectionCommandInput(id, name)

# Uses optional arguments.
returnValue = commandInputs_var.addDirectionCommandInput(id, name, resourceFolder)
```

## Return Value

| Type | Description |
|----|----|
| [DirectionCommandInput](DirectionCommandInput.md) | Returns the created DirectionCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| resourceFolder | string | Specifies the folder that contains the icon to use for the input. This is an optional argument. The input is shown as a check box if the resource folder is not set. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument whose default value is "". |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

