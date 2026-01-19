# UserInterface.activeSelectionChanged Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

This event fires whenever the contents of the active selection changes. This occurs as the user selects or unselects entities while using the Fusion Select command. The Select command is the default command that is always running if no other command is active. Pressing Escape terminates the currently active command and starts the Select command. If the Select command is running and you press Escape, it terminates the current Select command and starts a new one.  

This event is only associated with the selection associated with the Select command and does not fire when any other command is running. The event fires when there is any change to the active selection, including when the selection is cleared when the Select command is terminated. It is also fired when the user clicks in an open area of the canvas to clear the current selection.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "userInterface_var" is a variable referencing a UserInterface object.
# "MyActiveSelectionChangedHandler" is the name of the class that handles the event.
onActiveSelectionChanged = MyActiveSelectionChangedHandler()
userInterface_var.activeSelectionChanged.add(onActiveSelectionChanged)
handlers.append(onActiveSelectionChanged)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the activeSelectionChanged event.
class MyActiveSelectionChangedHandler(adsk.core.ActiveSelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ActiveSelectionEventArgs):
        # Code to react to the event.
        app.log('In MyActiveSelectionChangedHandler event handler.')
```

## Property Value

This is an event property that returns an [ActiveSelectionEvent](ActiveSelectionEvent.md).

## Version

Introduced in version August 2020  

