# Command.keyDown Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when a key on the keyboard is pressed down.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "command_var" is a variable referencing a Command object.
# "MyKeyDownHandler" is the name of the class that handles the event.
onKeyDown = MyKeyDownHandler()
command_var.keyDown.add(onKeyDown)
handlers.append(onKeyDown)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the keyDown event.
class MyKeyDownHandler(adsk.core.KeyboardEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.KeyboardEventArgs):
        # Code to react to the event.
        app.log('In MyKeyDownHandler event handler.')
```

## Property Value

This is an event property that returns a [KeyboardEvent](KeyboardEvent.md).

## Version

Introduced in version August 2014  

