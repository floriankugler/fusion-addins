# CAM.setupChanged Event

Parent Object: [CAM](CAM.md)  

## Description

The SetupChanged event fires when a setup is modified.

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
# "MySetupChangedHandler" is the name of the class that handles the event.
onSetupChanged = MySetupChangedHandler()
cAM_var.setupChanged.add(onSetupChanged)
handlers.append(onSetupChanged)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the setupChanged event.
class MySetupChangedHandler(adsk.cam.SetupChangeEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.cam.SetupChangeEventArgs):
        # Code to react to the event.
        app.log('In MySetupChangedHandler event handler.')
```

## Property Value

This is an event property that returns a [SetupChangeEvent](SetupChangeEvent.md).

## Version

Introduced in version April 2023  

