# WebRequestEvent.remove Method

Parent Object: [WebRequestEvent](WebRequestEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"webRequestEvent_var" is a variable referencing a [WebRequestEvent](WebRequestEvent.md) object.

```python
returnValue = webRequestEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [WebRequestEventHandler](WebRequestEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version May 2016  

