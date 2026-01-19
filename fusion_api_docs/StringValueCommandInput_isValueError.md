# StringValueCommandInput.isValueError Property

Parent Object: [StringValueCommandInput](StringValueCommandInput.md)  

## Description

Specifies if the current value shown is valid or not. Any string is valid for a StringValueCommandInput, but you many have some criteria that the string needs to meet for it to be valid in your application. You use the command's validateInputs event to verify that inputs are valid and control whether the "OK" button is enabled or not, and you can also set this property on specific StringValueCommandInputs objects to indicate to the user that a specific value is not correct. When this property is true, Fusion will change the color of the text to red to indicate to the user there is a problem.

## Syntax

"stringValueCommandInput_var" is a variable referencing a StringValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = stringValueCommandInput_var.isValueError

# Set the value of the property.
stringValueCommandInput_var.isValueError = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version April 2017  

