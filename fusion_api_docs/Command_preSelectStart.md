# Command.preSelectStart Event

Parent Object: [Command](Command.md)  

## Description

As the mouse moves over entities in the graphics window, entities valid for selection are highlighted. Before an entity is highlighted, Fusion determines if it is a valid selectable entity using the selection filter defined on the SelectionCommandInput and the preSelect event of the command. The preSelectStart event fires when the mouse first moves over an entity valid for selection. You can obtain the entity and mouse position from the Selection object returned by the selection property of the SelectionEventArgs object provided through the event.  

Some related events are the preSelectMouseMove event, which fires as the mouse moves across the entity, and the preSelectEnd event, which fires when the mouse moves off the entity.

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
# "MyPreSelectStartHandler" is the name of the class that handles the event.
onPreSelectStart = MyPreSelectStartHandler()
command_var.preSelectStart.add(onPreSelectStart)
handlers.append(onPreSelectStart)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the preSelectStart event.
class MyPreSelectStartHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.SelectionEventArgs):
        # Code to react to the event.
        app.log('In MyPreSelectStartHandler event handler.')
```

## Property Value

This is an event property that returns a [SelectionEvent](SelectionEvent.md).

## Version

Introduced in version May 2022  

