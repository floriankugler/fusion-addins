# CAM.setupDeactivated Event

Parent Object: [CAM](CAM.md)  

## Description

The SetupDeactivated event fires when a setup is deactivated.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "cAM_var" is a variable referencing a CAM object.
# "MySetupDeactivatedHandler" is the name of the class that handles the event.
onSetupDeactivated = MySetupDeactivatedHandler()
cAM_var.setupDeactivated.add(onSetupDeactivated)
handlers.append(onSetupDeactivated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the setupDeactivated event.
class MySetupDeactivatedHandler(adsk.cam.SetupEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.cam.SetupEventArgs):
        # Code to react to the event.
        app.log('In MySetupDeactivatedHandler event handler.')
```

## Property Value

This is an event property that returns a [SetupEvent](SetupEvent.md).

## Version

Introduced in version April 2023  

