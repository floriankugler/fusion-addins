# CAM.setupActivating Event

Parent Object: [CAM](CAM.md)  

## Description

The SetupActivating event fires before a setup is activated.

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
# "MySetupActivatingHandler" is the name of the class that handles the event.
onSetupActivating = MySetupActivatingHandler()
cAM_var.setupActivating.add(onSetupActivating)
handlers.append(onSetupActivating)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the setupActivating event.
class MySetupActivatingHandler(adsk.cam.SetupEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.cam.SetupEventArgs):
        # Code to react to the event.
        app.log('In MySetupActivatingHandler event handler.')
```

## Property Value

This is an event property that returns a [SetupEvent](SetupEvent.md).

## Version

Introduced in version April 2023  

