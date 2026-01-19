# CustomFeatureEventHandler.notify Method

Parent Object: [CustomFeatureEventHandler](CustomFeatureEventHandler.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The function called by Fusion when the associated event is fired.

## Syntax

"customFeatureEventHandler_var" is a variable referencing a [CustomFeatureEventHandler](CustomFeatureEventHandler.md) object.

```python
returnValue = customFeatureEventHandler_var.notify(eventArgs)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| eventArgs | [CustomFeatureEventArgs](CustomFeatureEventArgs.md) | Returns an object that provides access to additional information associated with the event. |

## Version

Introduced in version January 2021  

