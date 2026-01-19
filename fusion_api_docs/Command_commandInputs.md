# Command.commandInputs Property

Parent Object: [Command](Command.md)  

## Description

Gets the associated CommandInputs object which provides the ability to create new command inputs and provides access to any existing inputs that have already been created for this command.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.commandInputs
```

## Property Value

This is a read only property whose value is a [CommandInputs](CommandInputs.md).

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

