# Application.documentActivating Event

Parent Object: [Application](Application.md)  

## Description

The DocumentActivating event fires at the VERY start of a document being activated.

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
# "MyDocumentActivatingHandler" is the name of the class that handles the event.
onDocumentActivating = MyDocumentActivatingHandler()
application_var.documentActivating.add(onDocumentActivating)
handlers.append(onDocumentActivating)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the documentActivating event.
class MyDocumentActivatingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DocumentEventArgs):
        # Code to react to the event.
        app.log('In MyDocumentActivatingHandler event handler.')
```

## Property Value

This is an event property that returns a [DocumentEvent](DocumentEvent.md).

## Samples

| Name | Description |
|----|----|
| [Application Event API Sample](ApplicationEventSample_Sample.md) | Add-In that demonstrates application events. To use this sample, create a new folder using the name you want to use for the new add-in. Inside the folder, create a new file that is the same name as the folder but has a .py extension. Copy the code below into the .py file. Create another file that is the same name as the folder but has a .manifest extension and copy the JSON data below into that file. { "autodeskProduct": "Fusion360", "type": "addin", "author": "", "description": { "": "" }, "supportedOS": "windows\|mac", "editEnabled": true } Run the "Scripts and Add-Ins" command and click the green plus button near the top of the dialog. Browse to the location where you created the folder and select the folder. The add-in should now be displayed in the list of add-ins on the "Add-Ins" tab of the dialog. Select the add-in and click the "Run" button. This will load the add-in and when any of the application events occurr that it is watching for it will report them in the TEXT COMMAND window. |

## Version

Introduced in version May 2017  

