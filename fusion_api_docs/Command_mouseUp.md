# Command.mouseUp Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when a mouse button is released.

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
# "MyMouseUpHandler" is the name of the class that handles the event.
onMouseUp = MyMouseUpHandler()
command_var.mouseUp.add(onMouseUp)
handlers.append(onMouseUp)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mouseUp event.
class MyMouseUpHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MouseEventArgs):
        # Code to react to the event.
        app.log('In MyMouseUpHandler event handler.')
```

## Property Value

This is an event property that returns a [MouseEvent](MouseEvent.md).

## Version

Introduced in version August 2014  

