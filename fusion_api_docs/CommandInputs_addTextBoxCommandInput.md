# CommandInputs.addTextBoxCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a text box input to the command.

## Remarks

This method has been retired and replaced by the addSimpleTextBoxCommandInput and addFormattedTextBoxCommandInput methods. This method will continue to work as it did, but there were problems with the design that necessitated breaking it into two different types of text boxes. The simple text box cannot be formatted, but is editable by the user. The contents of a formatted text box can be defined using HTML but cannot be edited by the user.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addTextBoxCommandInput(id, name, formattedText, numRows, isReadOnly)
```

## Return Value

| Type | Description |
|----|----|
| [TextBoxCommandInput](TextBoxCommandInput.md) | Returns the created TextBoxCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. If an empty string is provided then no name will be displayed and the text box will span the width of the command dialog. |
| formattedText | string | Specifies the formatted text to display in the input. For example, you can use basic html formatting such as Bold, Italic, and   for a line break. It also supports hyperlinks, which when clicked by the user, Fusion will open the specified URL in the default browser. Hyperlinks are defined using the  tag such as "You are using Autodesk's Fusion.". If you are using HTML formatting in your text, it's best to set the text box to be read-only. However, if you want to use the text box as a way to get input from the user, it's best to use simple text so not HTML formatting is assumed. To do this, use an empty string for this argument and then set the text using the text property after the input is created. When the text property is used any HTML formatting is ignored and the text is treated as basics text. This can be useful if you're using the text box to have the user enter HTML code so it's treated as a simple string. |
| numRows | integer | Specifies the height of the text box as defined by the number of rows of text that can be displayed. If the text is larger than will fit in the box a scroll bar will automatically be displayed. |
| isReadOnly | boolean | Specifies if the text box is read-only or not. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

