# Command.preSelectEnd Event

Parent Object: [Command](Command.md)  

## Description

This event fires when the moused is moved away from an entity that was in a pre-select state. If your add-in has done something in reaction to the preSelect event, like draw some custom graphics, this event provides the notification to clean up whatever you've done that's associated with the current pre-select.  

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
# "MyPreSelectEndHandler" is the name of the class that handles the event.
onPreSelectEnd = MyPreSelectEndHandler()
command_var.preSelectEnd.add(onPreSelectEnd)
handlers.append(onPreSelectEnd)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the preSelectEnd event.
class MyPreSelectEndHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MyPreSelectEndHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version April 2019  

