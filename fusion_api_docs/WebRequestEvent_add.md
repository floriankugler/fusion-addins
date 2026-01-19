# WebRequestEvent.add Method

Parent Object: [WebRequestEvent](WebRequestEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"webRequestEvent_var" is a variable referencing a [WebRequestEvent](WebRequestEvent.md) object.

```python
returnValue = webRequestEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [WebRequestEventHandler](WebRequestEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version May 2016  

