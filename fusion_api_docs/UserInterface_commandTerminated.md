# UserInterface.commandTerminated Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

Gets an event that is fired when a command is terminated.

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
# "MyCommandTerminatedHandler" is the name of the class that handles the event.
onCommandTerminated = MyCommandTerminatedHandler()
userInterface_var.commandTerminated.add(onCommandTerminated)
handlers.append(onCommandTerminated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the commandTerminated event.
class MyCommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ApplicationCommandEventArgs):
        # Code to react to the event.
        app.log('In MyCommandTerminatedHandler event handler.')
```

## Property Value

This is an event property that returns an [ApplicationCommandEvent](ApplicationCommandEvent.md).

## Version

Introduced in version November 2015  

