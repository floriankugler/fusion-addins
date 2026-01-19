# HttpRequest.completed Event

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

The completed event fires when the request has completed. This event will fire on successful or failure.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "httpRequest_var" is a variable referencing a HttpRequest object.
# "MyCompletedHandler" is the name of the class that handles the event.
onCompleted = MyCompletedHandler()
httpRequest_var.completed.add(onCompleted)
handlers.append(onCompleted)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the completed event.
class MyCompletedHandler(adsk.core.HttpEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.HttpEventArgs):
        # Code to react to the event.
        app.log('In MyCompletedHandler event handler.')
```

## Property Value

This is an event property that returns a [HttpEvent](HttpEvent.md).

## Version

Introduced in version January 2024  

