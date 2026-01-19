# Application.openedFromURL Event

Parent Object: [Application](Application.md)  

## Description

The openedFromURL event fires after the user has clicked a link in a web page that uses the Fusion protocol handler to create a new using an existing file as the initial contents and that operation has completed.

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
# "MyOpenedFromURLHandler" is the name of the class that handles the event.
onOpenedFromURL = MyOpenedFromURLHandler()
application_var.openedFromURL.add(onOpenedFromURL)
handlers.append(onOpenedFromURL)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the openedFromURL event.
class MyOpenedFromURLHandler(adsk.core.WebRequestEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WebRequestEventArgs):
        # Code to react to the event.
        app.log('In MyOpenedFromURLHandler event handler.')
```

## Property Value

This is an event property that returns a [WebRequestEvent](WebRequestEvent.md).

## Version

Introduced in version May 2016  

