# AngleValueCommandInput.hasMinimumValue Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets and sets if there is a minimum value for this command input. When setting this property, it is only valid to set it to False to remove the minimum value. Setting the minimumValue property will result in this property being set to True.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.hasMinimumValue

# Set the value of the property.
angleValueCommandInput_var.hasMinimumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2017  

