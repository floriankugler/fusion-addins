# CommandInputs.addImageCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new Image input to the command.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addImageCommandInput(id, name, imageFile)
```

## Return Value

| Type | Description |
|----|----|
| [ImageCommandInput](ImageCommandInput.md) | Returns the created ImageCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this Image as seen in the dialog. If a name is not specified (an empty string), the image will be left justified within the dialog. If a name is specified it will appear as a left justified label aligned with the other command input labels, and the left side of the image will be aligned with the other command input controls. |
| imageFile | string | The full path and file name of the image file. Supported image format is .png Images are displayed in the command dialog using their actual size. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

