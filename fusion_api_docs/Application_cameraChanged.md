# Application.cameraChanged Event

Parent Object: [Application](Application.md)  

## Description

The cameraChanged event fires immediately after a change in the camera has been made. Camera changes happen when user changes the view by rotating, zooming in or out, panning, changing from parallel to perspective, or when the extents of the viewport changes.  

You can add or remove event handlers from the CameraEvent.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "application_var" is a variable referencing an Application object.
# "MyCameraChangedHandler" is the name of the class that handles the event.
onCameraChanged = MyCameraChangedHandler()
application_var.cameraChanged.add(onCameraChanged)
handlers.append(onCameraChanged)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the cameraChanged event.
class MyCameraChangedHandler(adsk.core.CameraEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.CameraEventArgs):
        # Code to react to the event.
        app.log('In MyCameraChangedHandler event handler.')
```

## Property Value

This is an event property that returns a [CameraEvent](CameraEvent.md).

## Version

Introduced in version December 2017  

