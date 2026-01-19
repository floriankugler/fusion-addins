# Command.mouseDoubleClick Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the mouse is double-clicked, (clicked twice within the time specified by a system setting.)

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
# "MyMouseDoubleClickHandler" is the name of the class that handles the event.
onMouseDoubleClick = MyMouseDoubleClickHandler()
command_var.mouseDoubleClick.add(onMouseDoubleClick)
handlers.append(onMouseDoubleClick)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mouseDoubleClick event.
class MyMouseDoubleClickHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MouseEventArgs):
        # Code to react to the event.
        app.log('In MyMouseDoubleClickHandler event handler.')
```

## Property Value

This is an event property that returns a [MouseEvent](MouseEvent.md).

## Version

Introduced in version August 2014  

