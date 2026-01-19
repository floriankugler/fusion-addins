# Command.mouseMove Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the mouse is moved.

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
# "MyMouseMoveHandler" is the name of the class that handles the event.
onMouseMove = MyMouseMoveHandler()
command_var.mouseMove.add(onMouseMove)
handlers.append(onMouseMove)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mouseMove event.
class MyMouseMoveHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MouseEventArgs):
        # Code to react to the event.
        app.log('In MyMouseMoveHandler event handler.')
```

## Property Value

This is an event property that returns a [MouseEvent](MouseEvent.md).

## Version

Introduced in version August 2014  

