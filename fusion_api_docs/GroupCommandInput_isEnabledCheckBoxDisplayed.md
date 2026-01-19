# GroupCommandInput.isEnabledCheckBoxDisplayed Property

Parent Object: [GroupCommandInput](GroupCommandInput.md)  

## Description

Gets or sets if this group has a check-box for enabling/disabling the group. If this is a sub-group of another group and the isEnabledCheckBoxDisplayed property is set to false then the isExpanded property must be set to true.

## Syntax

"groupCommandInput_var" is a variable referencing a GroupCommandInput object.  

```python
# Get the value of the property.
propertyValue = groupCommandInput_var.isEnabledCheckBoxDisplayed

# Set the value of the property.
groupCommandInput_var.isEnabledCheckBoxDisplayed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

