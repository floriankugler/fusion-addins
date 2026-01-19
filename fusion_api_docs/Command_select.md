# Command.select Event

Parent Object: [Command](Command.md)  

## Description

This even fires when the user selects an entity. This is different from the preselect where an entity is shown as being available for selection as the mouse passes over the entity. This is the actual selection where the user has clicked the mouse on the entity.  

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
# "MySelectHandler" is the name of the class that handles the event.
onSelect = MySelectHandler()
command_var.select.add(onSelect)
handlers.append(onSelect)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the select event.
class MySelectHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MySelectHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version April 2019  

