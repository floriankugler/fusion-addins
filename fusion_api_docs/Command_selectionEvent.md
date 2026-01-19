# Command.selectionEvent Event

Parent Object: [Command](Command.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Provides a notification when the mouse passes over an entity allowing you to determine if the entity should be available for selection or not.

## Remarks

This event has been retired. Equivalent functionality is provide by the preSelect event.

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
# "MySelectionEventHandler" is the name of the class that handles the event.
onSelectionEvent = MySelectionEventHandler()
command_var.selectionEvent.add(onSelectionEvent)
handlers.append(onSelectionEvent)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the selectionEvent event.
class MySelectionEventHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MySelectionEventHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version June 2015  
Retired in version July 2022  

