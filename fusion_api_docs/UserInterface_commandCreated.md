# UserInterface.commandCreated Event

Parent Object: [UserInterface](UserInterface.md)  

## Description

The commandCreated event fires immediately after the command is created.

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
# "MyCommandCreatedHandler" is the name of the class that handles the event.
onCommandCreated = MyCommandCreatedHandler()
userInterface_var.commandCreated.add(onCommandCreated)
handlers.append(onCommandCreated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the commandCreated event.
class MyCommandCreatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ApplicationCommandEventArgs):
        # Code to react to the event.
        app.log('In MyCommandCreatedHandler event handler.')
```

## Property Value

This is an event property that returns an [ApplicationCommandEvent](ApplicationCommandEvent.md).

## Version

Introduced in version November 2015  

