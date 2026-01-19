# Application.dataFileCopyComplete Event

Parent Object: [Application](Application.md)  

## Description

The dataFileCopyComplete event fires when a data file copy has completed including any PIM Data copy.

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
# "MyDataFileCopyCompleteHandler" is the name of the class that handles the event.
onDataFileCopyComplete = MyDataFileCopyCompleteHandler()
application_var.dataFileCopyComplete.add(onDataFileCopyComplete)
handlers.append(onDataFileCopyComplete)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the dataFileCopyComplete event.
class MyDataFileCopyCompleteHandler(adsk.core.DataEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DataEventArgs):
        # Code to react to the event.
        app.log('In MyDataFileCopyCompleteHandler event handler.')
```

## Property Value

This is an event property that returns a [DataEvent](DataEvent.md).

## Version

Introduced in version October 2023  

