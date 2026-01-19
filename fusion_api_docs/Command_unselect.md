# Command.unselect Event

Parent Object: [Command](Command.md)  

## Description

This even fires when the user unselects an entity by clicking the mouse again on selected entity or canceling previous selection.  

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
# "MyUnselectHandler" is the name of the class that handles the event.
onUnselect = MyUnselectHandler()
command_var.unselect.add(onUnselect)
handlers.append(onUnselect)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the unselect event.
class MyUnselectHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MyUnselectHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version April 2019  

