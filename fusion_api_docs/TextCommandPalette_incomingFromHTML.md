# TextCommandPalette.incomingFromHTML Event

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

This event is fired when the JavaScript associated with the HTML calls the adsk.fusionSendData function. This allows the HTML to communicate with the add-in by passing information to the add-in.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "textCommandPalette_var" is a variable referencing a TextCommandPalette object.
# "MyIncomingFromHTMLHandler" is the name of the class that handles the event.
onIncomingFromHTML = MyIncomingFromHTMLHandler()
textCommandPalette_var.incomingFromHTML.add(onIncomingFromHTML)
handlers.append(onIncomingFromHTML)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the incomingFromHTML event.
class MyIncomingFromHTMLHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.HTMLEventArgs):
        # Code to react to the event.
        app.log('In MyIncomingFromHTMLHandler event handler.')
```

## Property Value

This is an event property that returns a [HTMLEvent](HTMLEvent.md).

## Version

Introduced in version August 2017  

