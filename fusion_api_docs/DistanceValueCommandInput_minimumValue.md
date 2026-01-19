# DistanceValueCommandInput.minimumValue Property

Parent Object: [DistanceValueCommandInput](DistanceValueCommandInput.md)  

## Description

Gets and sets minimum value, if any, that the value can be. When getting this property you should first check the hasMinimumValue property to see if this property applies. Also, the isMinimumValueInclusive indicates if the minimum includes this value or will be up to this value.  

Setting this value will change the isMinimumValueInclusive to True and the hasMinimumValue property to True if hasMinimumValue is currently False, otherwise it will just update the value.

## Syntax

"distanceValueCommandInput_var" is a variable referencing a DistanceValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = distanceValueCommandInput_var.minimumValue

# Set the value of the property.
distanceValueCommandInput_var.minimumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

