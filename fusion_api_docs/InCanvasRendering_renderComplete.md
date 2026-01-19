# InCanvasRendering.renderComplete Event

Parent Object: [InCanvasRendering](InCanvasRendering.md)  

## Description

The RenderEvent event fires when the rendering has reached the quality that was specified when the rendering started. This event is only fired when using advanced rendering (the isAdvanced property is True). To save the finished rendering, use the saveImage method.  

You can add or remove event handlers from the RenderEvent.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "inCanvasRendering_var" is a variable referencing an InCanvasRendering object.
# "MyRenderCompleteHandler" is the name of the class that handles the event.
onRenderComplete = MyRenderCompleteHandler()
inCanvasRendering_var.renderComplete.add(onRenderComplete)
handlers.append(onRenderComplete)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the renderComplete event.
class MyRenderCompleteHandler(adsk.fusion.RenderEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.fusion.RenderEventArgs):
        # Code to react to the event.
        app.log('In MyRenderCompleteHandler event handler.')
```

## Property Value

This is an event property that returns a [RenderEvent](RenderEvent.md).

## Version

Introduced in version September 2023  

