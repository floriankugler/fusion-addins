# CommandDefinition.commandCreated Event

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

This event is fired when the associated control is manipulated by the user. A new Command object is created and passed back through this event which you can then use to interact with the user to get any input the command requires.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "commandDefinition_var" is a variable referencing a CommandDefinition object.
# "MyCommandCreatedHandler" is the name of the class that handles the event.
onCommandCreated = MyCommandCreatedHandler()
commandDefinition_var.commandCreated.add(onCommandCreated)
handlers.append(onCommandCreated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the commandCreated event.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        # Code to react to the event.
        app.log('In MyCommandCreatedHandler event handler.')
```

## Property Value

This is an event property that returns a [CommandCreatedEvent](CommandCreatedEvent.md).

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

