# CustomFeatureDefinition.customFeatureCompute Event

Parent Object: [CustomFeatureDefinition](CustomFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The customFeatureCompute event fires when Fusion is computing the timeline and reaches the custom feature. The event is fired if any of the dependencies of the custom feature have changed. You can modify the results of your custom feature based on the dependencies.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "customFeatureDefinition_var" is a variable referencing a CustomFeatureDefinition object.
# "MyCustomFeatureComputeHandler" is the name of the class that handles the event.
onCustomFeatureCompute = MyCustomFeatureComputeHandler()
customFeatureDefinition_var.customFeatureCompute.add(onCustomFeatureCompute)
handlers.append(onCustomFeatureCompute)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the customFeatureCompute event.
class MyCustomFeatureComputeHandler(adsk.fusion.CustomFeatureEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.fusion.CustomFeatureEventArgs):
        # Code to react to the event.
        app.log('In MyCustomFeatureComputeHandler event handler.')
```

## Property Value

This is an event property that returns a [CustomFeatureEvent](CustomFeatureEvent.md).

## Version

Introduced in version January 2021  

