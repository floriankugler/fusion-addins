# Command.deactivate Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the command is deactivated. The command still exists and could still be activated again.

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
# "MyDeactivateHandler" is the name of the class that handles the event.
onDeactivate = MyDeactivateHandler()
command_var.deactivate.add(onDeactivate)
handlers.append(onDeactivate)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the deactivate event.
class MyDeactivateHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CommandEventArgs):
        # Code to react to the event.
        app.log('In MyDeactivateHandler event handler.')
```

## Property Value

This is an event property that returns a [CommandEvent](CommandEvent.md).

## Return Value

| Type | Description |
|----|----|
| [CommandEvent](CommandEvent.md) | Returns a CommandEvent object that is used to connect and release from the event. |

## Version

Introduced in version August 2014  

