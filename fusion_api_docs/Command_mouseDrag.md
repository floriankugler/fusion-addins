# Command.mouseDrag Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when the mouse is in drag mode, (being moved while a button is pressed).

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
# "MyMouseDragHandler" is the name of the class that handles the event.
onMouseDrag = MyMouseDragHandler()
command_var.mouseDrag.add(onMouseDrag)
handlers.append(onMouseDrag)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mouseDrag event.
class MyMouseDragHandler(adsk.core.MouseEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MouseEventArgs):
        # Code to react to the event.
        app.log('In MyMouseDragHandler event handler.')
```

## Property Value

This is an event property that returns a [MouseEvent](MouseEvent.md).

## Version

Introduced in version August 2014  

