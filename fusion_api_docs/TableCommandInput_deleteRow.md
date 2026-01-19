# TableCommandInput.deleteRow Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Deletes the specified row. The following rows will be shifted up. The row and the command inputs it contains are deleted. To temporarily hide a row you can set the visibility of all of the command inputs it contains to be invisible. If all inputs are invisible the row will automatically be hidden.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.

```python
returnValue = tableCommandInput_var.deleteRow(row)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| row | integer | The row to delete where valid values are 0 to the number of rows minus 1. A value of 0 will delete the first row. A value greater than the number of rows will delete the last row. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2016  

