# RenderEvent.add Method

Parent Object: [RenderEvent](RenderEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"renderEvent_var" is a variable referencing a [RenderEvent](RenderEvent.md) object.

```python
returnValue = renderEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [RenderEventHandler](RenderEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version September 2023  

