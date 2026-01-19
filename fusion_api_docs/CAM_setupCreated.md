# CAM.setupCreated Event

Parent Object: [CAM](CAM.md)  

## Description

The SetupCreated event fires when a new setup is created.

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
# "MySetupCreatedHandler" is the name of the class that handles the event.
onSetupCreated = MySetupCreatedHandler()
cAM_var.setupCreated.add(onSetupCreated)
handlers.append(onSetupCreated)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the setupCreated event.
class MySetupCreatedHandler(adsk.cam.SetupEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.cam.SetupEventArgs):
        # Code to react to the event.
        app.log('In MySetupCreatedHandler event handler.')
```

## Property Value

This is an event property that returns a [SetupEvent](SetupEvent.md).

## Version

Introduced in version April 2023  

