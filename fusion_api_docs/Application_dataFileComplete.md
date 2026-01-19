# Application.dataFileComplete Event

Parent Object: [Application](Application.md)  

## Description

The dataFileComplete event fires when a data file upload has completed including any cloud side translations.

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
# "MyDataFileCompleteHandler" is the name of the class that handles the event.
onDataFileComplete = MyDataFileCompleteHandler()
application_var.dataFileComplete.add(onDataFileComplete)
handlers.append(onDataFileComplete)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the dataFileComplete event.
class MyDataFileCompleteHandler(adsk.core.DataEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DataEventArgs):
        # Code to react to the event.
        app.log('In MyDataFileCompleteHandler event handler.')
```

## Property Value

This is an event property that returns a [DataEvent](DataEvent.md).

## Samples

| Name | Description |
|----|----|
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version January 2022  

