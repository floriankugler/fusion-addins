# Application.documentOpened Event

Parent Object: [Application](Application.md)  

## Description

The DocumentOpened event fires at the VERY end of a document being opened so the Document object is available to be used.  

When a document is opened that references other documents, only the top-level document will cause the documentOpened event to be fired. You can access the referenced documents by using the documentReferences property of the Document object.

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
# "MyDocumentOpenedHandler" is the name of the class that handles the event.
onDocumentOpened = MyDocumentOpenedHandler()
application_var.documentOpened.add(onDocumentOpened)
handlers.append(onDocumentOpened)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the documentOpened event.
class MyDocumentOpenedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DocumentEventArgs):
        # Code to react to the event.
        app.log('In MyDocumentOpenedHandler event handler.')
```

## Property Value

This is an event property that returns a [DocumentEvent](DocumentEvent.md).

## Version

Introduced in version August 2014  

