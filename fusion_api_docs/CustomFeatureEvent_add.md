# CustomFeatureEvent.add Method

Parent Object: [CustomFeatureEvent](CustomFeatureEvent.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Add a handler to be notified when the file event occurs.

## Syntax

"customFeatureEvent_var" is a variable referencing a [CustomFeatureEvent](CustomFeatureEvent.md) object.

```python
returnValue = customFeatureEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CustomFeatureEventHandler](CustomFeatureEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version January 2021  

