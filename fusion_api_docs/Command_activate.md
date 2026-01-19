# Command.activate Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the command is first activated or re-activated after being suspended.

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
# "MyActivateHandler" is the name of the class that handles the event.
onActivate = MyActivateHandler()
command_var.activate.add(onActivate)
handlers.append(onActivate)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the activate event.
class MyActivateHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CommandEventArgs):
        # Code to react to the event.
        app.log('In MyActivateHandler event handler.')
```

## Property Value

This is an event property that returns a [CommandEvent](CommandEvent.md).

## Return Value

| Type | Description |
|----|----|
| [CommandEvent](CommandEvent.md) | Returns a CommandEvent object that is used to connect and release from the event. |

## Version

Introduced in version August 2014  

