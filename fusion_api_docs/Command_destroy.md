# Command.destroy Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the command is destroyed. The command is destroyed and can be cleaned up.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "command_var" is a variable referencing a Command object.
# "MyDestroyHandler" is the name of the class that handles the event.
onDestroy = MyDestroyHandler()
command_var.destroy.add(onDestroy)
handlers.append(onDestroy)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the destroy event.
class MyDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CommandEventArgs):
        # Code to react to the event.
        app.log('In MyDestroyHandler event handler.')
```

## Property Value

This is an event property that returns a [CommandEvent](CommandEvent.md).

## Return Value

| Type | Description |
|----|----|
| [CommandEvent](CommandEvent.md) | Returns a CommandEvent object that is used to connect and release from the event. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

