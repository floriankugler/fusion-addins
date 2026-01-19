# CommandInputs.addTableCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new table command input to the command.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addTableCommandInput(id, name, numberOfColumns, columnRatio)
```

## Return Value

| Type | Description |
|----|----|
| [TableCommandInput](TableCommandInput.md) | Returns the created TableCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed name of this command as seen in the dialog. |
| numberOfColumns | integer | This argument is no longer used. The number of columns displayed is inferred by the number of columns that contain command inputs. As you add command inputs to the table the display of the table will adjust to show all of the columns that contain a command input. |
| columnRatio | string | Sets the width ratio of the columns. This is defined using a string such as "1:1:1" where this defines that the first three columns are all the same width. A value of "2:1" defines that the first column is twice the width of the second. If the table has more columns than are defined by this property, they will automatically default to a value of 1. If this property defines the width of more columns than are displayed, the extra definitions are ignored. You can also specify 0 as a column width and this will have the effect of hiding that column. Setting a column width to 0 does not delete the column or the command inputs but only hides them so they can be turned back on at a later time by resetting the column ratio. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |

## Version

Introduced in version September 2016  

