# DirectionCommandInput.isDirectionFlipped Property

Parent Object: [DirectionCommandInput](DirectionCommandInput.md)  

## Description

Gets and sets if the direction manipulator displayed is flipped (reversed 180 degrees as compared to the direction defined by the manipulatorDirection property). This is false for a newly created DirectionCommandInput.

## Syntax

"directionCommandInput_var" is a variable referencing a DirectionCommandInput object.  

```python
# Get the value of the property.
propertyValue = directionCommandInput_var.isDirectionFlipped

# Set the value of the property.
directionCommandInput_var.isDirectionFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2016  

