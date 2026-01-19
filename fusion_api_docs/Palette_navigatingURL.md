# Palette.navigatingURL Event

Parent Object: [Palette](Palette.md)  

## Description

This event is fired when a navigation event occurs on the page. This allows the add-in to determine how this navigation should be handled by the browser.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "palette_var" is a variable referencing a Palette object.
# "MyNavigatingURLHandler" is the name of the class that handles the event.
onNavigatingURL = MyNavigatingURLHandler()
palette_var.navigatingURL.add(onNavigatingURL)
handlers.append(onNavigatingURL)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the navigatingURL event.
class MyNavigatingURLHandler(adsk.core.NavigationEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.NavigationEventArgs):
        # Code to react to the event.
        app.log('In MyNavigatingURLHandler event handler.')
```

## Property Value

This is an event property that returns a [NavigationEvent](NavigationEvent.md).

## Version

Introduced in version March 2021  

