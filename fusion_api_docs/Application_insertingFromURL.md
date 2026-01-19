# Application.insertingFromURL Event

Parent Object: [Application](Application.md)  

## Description

The insertingFromURL event fires when the user has clicked a link in a web page that uses the Fusion protocol handler to insert a file as new component. This event is fired at the beginning of the request but before Fusion has take any action so that it's still possible to cancel the operation.

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
# "MyInsertingFromURLHandler" is the name of the class that handles the event.
onInsertingFromURL = MyInsertingFromURLHandler()
application_var.insertingFromURL.add(onInsertingFromURL)
handlers.append(onInsertingFromURL)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the insertingFromURL event.
class MyInsertingFromURLHandler(adsk.core.WebRequestEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WebRequestEventArgs):
        # Code to react to the event.
        app.log('In MyInsertingFromURLHandler event handler.')
```

## Property Value

This is an event property that returns a [WebRequestEvent](WebRequestEvent.md).

## Version

Introduced in version May 2016  

