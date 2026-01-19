# Command.preSelectMouseMove Event

Parent Object: [Command](Command.md)  

## Description

This event fires continually while the mouse is moved over an entity that is valid for selected.  

The entity and mouse position on the entity can be obtained through the Selection object returned through the selection property of the SelectionEventArgs object provided through the event.

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
# "MyPreSelectMouseMoveHandler" is the name of the class that handles the event.
onPreSelectMouseMove = MyPreSelectMouseMoveHandler()
command_var.preSelectMouseMove.add(onPreSelectMouseMove)
handlers.append(onPreSelectMouseMove)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the preSelectMouseMove event.
class MyPreSelectMouseMoveHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MyPreSelectMouseMoveHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version April 2019  

