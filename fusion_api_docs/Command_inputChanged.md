# Command.inputChanged Event

Parent Object: [Command](Command.md)  

## Description

Gets an event that is fired whenever an input value is changed.

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
# "MyInputChangedHandler" is the name of the class that handles the event.
onInputChanged = MyInputChangedHandler()
command_var.inputChanged.add(onInputChanged)
handlers.append(onInputChanged)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the inputChanged event.
class MyInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.InputChangedEventArgs):
        # Code to react to the event.
        app.log('In MyInputChangedHandler event handler.')
```

## Property Value

This is an event property that returns an [InputChangedEvent](InputChangedEvent.md).

## Return Value

| Type | Description |
|----|----|
| [InputChangedEvent](InputChangedEvent.md) | Returns an InputChangedEvent object that is used to connect and release from the event. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

