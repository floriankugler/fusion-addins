# Command.validateInputs Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired to allow you to check if the current state of the inputs are valid for execution.  

The timing of this event is indeterminate and not always tied to the editing of an input. There are cases where this isn't fired when an input is edited. This happens when an input is able to validate its content on its own. For example, if you enter an invalid value for a ValueCommandInput, it can evaluate this on its own, and as a result, the validate inputs event is not fired. Fusion will sometimes fire this event at other random times that are not tied to the edit of an input.  

If you want to be notified when an input changes, you should use the input changed event instead.

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
# "MyValidateInputsHandler" is the name of the class that handles the event.
onValidateInputs = MyValidateInputsHandler()
command_var.validateInputs.add(onValidateInputs)
handlers.append(onValidateInputs)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the validateInputs event.
class MyValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ValidateInputsEventArgs):
        # Code to react to the event.
        app.log('In MyValidateInputsHandler event handler.')
```

## Property Value

This is an event property that returns a [ValidateInputsEvent](ValidateInputsEvent.md).

## Version

Introduced in version August 2014  

