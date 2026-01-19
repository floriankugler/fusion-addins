# CommandInputs.addTabCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new Tab input to the command. Tab command inputs contain a set of command inputs and/or group command inputs

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addTabCommandInput(id, name)

# Uses optional arguments.
returnValue = commandInputs_var.addTabCommandInput(id, name, resourceFolder)
```

## Return Value

| Type | Description |
|----|----|
| [TabCommandInput](TabCommandInput.md) | Returns the created TabCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this tab as seen in the dialog. |
| resourceFolder | string | An optional parameter that specifies the folder that contains the image for the tab. If no name is specified (no text on tab), a resourceFolder containing the image to appear on the tab needs to be provided. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument whose default value is "". |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

