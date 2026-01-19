# Application.openingFromURL Event

Parent Object: [Application](Application.md)  

## Description

The openingFromURL event fires when the user has clicked a link in a web page that uses the Fusion protocol handler to create a new file using an existing file as the initial contents. This event is fired at the beginning of the request but before Fusion has take any action so that it's still possible to cancel the operation.

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
# "MyOpeningFromURLHandler" is the name of the class that handles the event.
onOpeningFromURL = MyOpeningFromURLHandler()
application_var.openingFromURL.add(onOpeningFromURL)
handlers.append(onOpeningFromURL)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the openingFromURL event.
class MyOpeningFromURLHandler(adsk.core.WebRequestEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WebRequestEventArgs):
        # Code to react to the event.
        app.log('In MyOpeningFromURLHandler event handler.')
```

## Property Value

This is an event property that returns a [WebRequestEvent](WebRequestEvent.md).

## Version

Introduced in version May 2016  

