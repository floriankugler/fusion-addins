# UserInterface.commandStarting Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

The commandStarting event fires when a request for a command to be executed has been received but before the command is executed. Through this event, it's possible to cancel the command from being executed.

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
# "MyCommandStartingHandler" is the name of the class that handles the event.
onCommandStarting = MyCommandStartingHandler()
userInterface_var.commandStarting.add(onCommandStarting)
handlers.append(onCommandStarting)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the commandStarting event.
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ApplicationCommandEventArgs):
        # Code to react to the event.
        app.log('In MyCommandStartingHandler event handler.')
```

## Property Value

This is an event property that returns an [ApplicationCommandEvent](ApplicationCommandEvent.md).

## Version

Introduced in version November 2015  

