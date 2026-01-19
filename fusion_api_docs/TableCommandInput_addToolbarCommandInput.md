# TableCommandInput.addToolbarCommandInput Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Adds a new command input to the toolbar at the bottom of the table.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.

```python
returnValue = tableCommandInput_var.addToolbarCommandInput(input)
```

## Return Value

| Type    | Description                                               |
|---------|-----------------------------------------------------------|
| boolean | Returns true if the command input was successfully added. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| input | [CommandInput](CommandInput.md) | Adds a command input to the toolbar at the bottom of the table. The inputs are displayed in the same order that they're added. The command input is created in the standard way but when it's added to the table using this method it will be displayed in the table instead of the main area of the dialog. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2016  

