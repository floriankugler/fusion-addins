# Command.mouseDragBegin Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when a mouse drag starts, (the mouse is pressed and moved).

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
# "MyMouseDragBeginHandler" is the name of the class that handles the event.
onMouseDragBegin = MyMouseDragBeginHandler()
command_var.mouseDragBegin.add(onMouseDragBegin)
handlers.append(onMouseDragBegin)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mouseDragBegin event.
class MyMouseDragBeginHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MouseEventArgs):
        # Code to react to the event.
        app.log('In MyMouseDragBeginHandler event handler.')
```

## Property Value

This is an event property that returns a [MouseEvent](MouseEvent.md).

## Version

Introduced in version August 2014  

