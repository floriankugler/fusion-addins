# CommandCreatedEventArgs.command Property

Parent Object: [CommandCreatedEventArgs](CommandCreatedEventArgs.md)  

## Description

Gets the newly created Command object that allows you to perform an action in response to the control being clicked.

## Syntax

"commandCreatedEventArgs_var" is a variable referencing a CommandCreatedEventArgs object.  

```python
# Get the value of the property.
propertyValue = commandCreatedEventArgs_var.command
```

## Property Value

This is a read only property whose value is a [Command](Command.md).

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

