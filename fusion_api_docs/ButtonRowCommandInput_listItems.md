# ButtonRowCommandInput.listItems Property

Parent Object: [ButtonRowCommandInput](ButtonRowCommandInput.md)  

## Description

Returns the ListItems object associated with this button row. You use this object to populate and interact with the buttons in the row. When adding items to a ButtonRowCommandInput, icons are required.

## Syntax

"buttonRowCommandInput_var" is a variable referencing a ButtonRowCommandInput object.  

```python
# Get the value of the property.
propertyValue = buttonRowCommandInput_var.listItems
```

## Property Value

This is a read only property whose value is a [ListItems](ListItems.md).

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

