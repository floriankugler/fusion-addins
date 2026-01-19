# TextCommandPalette.closed Event

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

This event is fired when the user clicks the "Close" button on the palette. You can choose if the "Close" button is available or not when you initially create the palette. When a palette is closed, it still exists but is change to invisible so you can still interact with it and retrieve any needed information and can make it visible again. Use the deleteMe method to delete the palette.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "textCommandPalette_var" is a variable referencing a TextCommandPalette object.
# "MyClosedHandler" is the name of the class that handles the event.
onClosed = MyClosedHandler()
textCommandPalette_var.closed.add(onClosed)
handlers.append(onClosed)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the closed event.
class MyClosedHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.UserInterfaceGeneralEventArgs):
        # Code to react to the event.
        app.log('In MyClosedHandler event handler.')
```

## Property Value

This is an event property that returns a [UserInterfaceGeneralEvent](UserInterfaceGeneralEvent.md).

## Version

Introduced in version August 2017  

