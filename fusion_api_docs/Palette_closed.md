# Palette.closed Event

Parent Object: [Palette](Palette.md)  

## Description

This event is fired when the user clicks the "Close" button on the palette. You can choose if the "Close" button is available or not when you initially create the palette. When a palette is closed, it still exists but is change to invisible so you can still interact with it and retrieve any needed information and can make it visible again. Use the deleteMe method to delete the palette.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "palette_var" is a variable referencing a Palette object.
# "MyClosedHandler" is the name of the class that handles the event.
onClosed = MyClosedHandler()
palette_var.closed.add(onClosed)
handlers.append(onClosed)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the closed event.
class MyClosedHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.UserInterfaceGeneralEventArgs):
        # Code to react to the event.
        app.log('In MyClosedHandler event handler.')
```

## Property Value

This is an event property that returns a [UserInterfaceGeneralEvent](UserInterfaceGeneralEvent.md).

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |

## Version

Introduced in version March 2017  

