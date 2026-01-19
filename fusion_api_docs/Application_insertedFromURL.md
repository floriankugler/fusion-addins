# Application.insertedFromURL Event

Parent Object: [Application](Application.md)  

## Description

The insertedFromURL event fires after the user has clicked a link in a web page that uses the Fusion protocol handler to insert a file as new component and that operation has completed.

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
# "MyInsertedFromURLHandler" is the name of the class that handles the event.
onInsertedFromURL = MyInsertedFromURLHandler()
application_var.insertedFromURL.add(onInsertedFromURL)
handlers.append(onInsertedFromURL)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the insertedFromURL event.
class MyInsertedFromURLHandler(adsk.core.WebRequestEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.WebRequestEventArgs):
        # Code to react to the event.
        app.log('In MyInsertedFromURLHandler event handler.')
```

## Property Value

This is an event property that returns a [WebRequestEvent](WebRequestEvent.md).

## Version

Introduced in version May 2016  

