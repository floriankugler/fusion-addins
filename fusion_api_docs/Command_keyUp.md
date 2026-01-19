# Command.keyUp Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired when a key on the keyboard goes up.

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
# "MyKeyUpHandler" is the name of the class that handles the event.
onKeyUp = MyKeyUpHandler()
command_var.keyUp.add(onKeyUp)
handlers.append(onKeyUp)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the keyUp event.
class MyKeyUpHandler(adsk.core.KeyboardEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.KeyboardEventArgs):
        # Code to react to the event.
        app.log('In MyKeyUpHandler event handler.')
```

## Property Value

This is an event property that returns a [KeyboardEvent](KeyboardEvent.md).

## Version

Introduced in version August 2014  

