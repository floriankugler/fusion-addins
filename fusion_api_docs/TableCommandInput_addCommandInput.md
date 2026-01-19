# TableCommandInput.addCommandInput Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Adds a command input to a particular cell in the table. Rows are automatically added to the table to able to contain the command input. The command input can span multiple columns within a row and spanning across multiple rows is not currently supported.  

The command input is created in the standard way but when it's added to the table using this method it will be displayed in the table instead of the main area of the dialog.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.

```python
# Uses no optional arguments.
returnValue = tableCommandInput_var.addCommandInput(input, row, column)

# Uses optional arguments.
returnValue = tableCommandInput_var.addCommandInput(input, row, column, rowSpan, columnSpan)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the association of the command input to the cell was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| input | [CommandInput](CommandInput.md) | The command input to associate to a cell. The command input is created in the standard way but when it's added to the table using this method it will be displayed in the table instead of the main area of the dialog. |
| row | integer | The row index of the cell where 0 is the first row. |
| column | integer | The column index of the cell where 0 is the first column. |
| rowSpan | integer | The number of additional rows that this input uses. The default value of 0 indicates that no additional rows are used. Row spanning is not currently supported so this value must always be 0. This is an optional argument whose default value is 0. |
| columnSpan | integer | The number of additional columns that this input uses. The default value of 0 indicates that no additional columns are used. This is an optional argument whose default value is 0. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |

## Version

Introduced in version September 2016  

