# Application.documentOpening Event

Parent Object: [Application](Application.md)  

## Description

The DocumentOpening event fires at the VERY start of a document being opened. There is no promise that the document will be opened, hence a documentOpened event may not follow.  

When a document is being opened that references other documents, only the top-level document will cause a documentOpening event to be fired.

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
# "MyDocumentOpeningHandler" is the name of the class that handles the event.
onDocumentOpening = MyDocumentOpeningHandler()
application_var.documentOpening.add(onDocumentOpening)
handlers.append(onDocumentOpening)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the documentOpening event.
class MyDocumentOpeningHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.DocumentEventArgs):
        # Code to react to the event.
        app.log('In MyDocumentOpeningHandler event handler.')
```

## Property Value

This is an event property that returns a [DocumentEvent](DocumentEvent.md).

## Version

Introduced in version August 2014  

