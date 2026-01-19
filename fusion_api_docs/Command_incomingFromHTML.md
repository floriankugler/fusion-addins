# Command.incomingFromHTML Event

Parent Object: [Command](Command.md)  

## Description

This event is fired when the JavaScript associated with the HTML displayed in a BrowserCommandInput calls the adsk.fusionSendData function and when the JavaScript responds to the sendInfoToHTML call. The HTMLEventArgs provided by the event indicates which BrowserCommandInput triggered the event.

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
# "MyIncomingFromHTMLHandler" is the name of the class that handles the event.
onIncomingFromHTML = MyIncomingFromHTMLHandler()
command_var.incomingFromHTML.add(onIncomingFromHTML)
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

Introduced in version July 2021  

