# Command.preSelect Event

Parent Object: [Command](Command.md)  

## Description

This event is used to be able to participate in the selection process in a dynamic way. When a user is selecting geometry, they move the mouse over the model and if the entity the mouse is currently over is valid for selection it will highlight indicating that it can be selected. This process of determining what is available for selection and highlighting it is referred to as the "preselect" behavior.  

You use functions on the SelectionCommandInput object to define what types of entities are selectable and in many cases this coarse level of specification is all that's needed, but in other cases you may need more control over the selection. For example, you might want to allow the user to selection construction planes and planar faces, which can easily be controlled by defining those as valid entities for selection in the SelectionCommandInput object. But if you only want to allow the user to select planes that are parallel then you need some dynamic control over the selection, which can be done using the preSelect event.  

In the example of selecting parallel planes, you would still set the valid selection types for the SelectionCommandInput to allow selection of construction planes and planar faces. This will limit the selection to only planes but any plane can still be selected. You'll also need to connect to the preSelect event for the command. As the user moves the mouse over any construction plane or planar face, the preSelect event will fire for the plane the mouse is current over. If no planes have yet been selected, then you allow the user to select this plane. If one or more planes have already selected, then in the preSelect event you'll check to see if the plane the mouse is over is parallel to the first plane already selected. If it is then you allow it to be selected. If it isn't parallel then you set the isSelectable property of the provided SelectEventArgs object to False so that it won't pre-highlight and won't be selectable.  

The entity and mouse position on the entity can be obtained through the Selection object returned through the selection property of the SelectionEventArgs object provided through the event.

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
# "MyPreSelectHandler" is the name of the class that handles the event.
onPreSelect = MyPreSelectHandler()
command_var.preSelect.add(onPreSelect)
handlers.append(onPreSelect)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the preSelect event.
class MyPreSelectHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MyPreSelectHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version April 2019  

