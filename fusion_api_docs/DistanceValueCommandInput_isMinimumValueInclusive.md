# DistanceValueCommandInput.isMinimumValueInclusive Property

Parent Object: [DistanceValueCommandInput](DistanceValueCommandInput.md)  

## Description

Gets and sets if the value of the input includes the minimum value or is up to the minimum value. For example, if the minimum value is zero and this property is True, the minimum value can be zero. If this is False, the minimum value must be greater than zero. When the minimum value is first defined using the minimumValue property, this property is set to True. The value returned by this property is only meaningful when the hasMinimumValue property returns True.

## Syntax

"distanceValueCommandInput_var" is a variable referencing a DistanceValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = distanceValueCommandInput_var.isMinimumValueInclusive

# Set the value of the property.
distanceValueCommandInput_var.isMinimumValueInclusive = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

