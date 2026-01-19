# Command.execute Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the command has completed gathering the required input and now needs to perform whatever action the command does.

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
# "MyExecuteHandler" is the name of the class that handles the event.
onExecute = MyExecuteHandler()
command_var.execute.add(onExecute)
handlers.append(onExecute)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the execute event.
class MyExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CommandEventArgs):
        # Code to react to the event.
        app.log('In MyExecuteHandler event handler.')
```

## Property Value

This is an event property that returns a [CommandEvent](CommandEvent.md).

## Return Value

| Type | Description |
|----|----|
| [CommandEvent](CommandEvent.md) | Returns a CommandEvent object that is used to connect and release from the event. |

## Version

Introduced in version August 2014  

