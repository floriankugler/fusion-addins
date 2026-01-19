# TableCommandInput.selectedRow Property

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Gets and sets which row is selected in the user-interface. A value of 0 indicates that the first row is selected. A value of -1 indicates that no row is selected.

## Syntax

"tableCommandInput_var" is a variable referencing a TableCommandInput object.  

```python
# Get the value of the property.
propertyValue = tableCommandInput_var.selectedRow

# Set the value of the property.
tableCommandInput_var.selectedRow = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2016  

