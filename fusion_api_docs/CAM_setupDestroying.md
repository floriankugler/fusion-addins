# CAM.setupDestroying Event

Parent Object: [CAM](CAM.md)  

## Description

The setupDestroying event fires before a setup is destroyed.

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
# "MySetupDestroyingHandler" is the name of the class that handles the event.
onSetupDestroying = MySetupDestroyingHandler()
cAM_var.setupDestroying.add(onSetupDestroying)
handlers.append(onSetupDestroying)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the setupDestroying event.
class MySetupDestroyingHandler(adsk.cam.SetupEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.cam.SetupEventArgs):
        # Code to react to the event.
        app.log('In MySetupDestroyingHandler event handler.')
```

## Property Value

This is an event property that returns a [SetupEvent](SetupEvent.md).

## Version

Introduced in version April 2023  

