# ApplicationEvent.remove Method

Parent Object: [ApplicationEvent](ApplicationEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"applicationEvent_var" is a variable referencing an [ApplicationEvent](ApplicationEvent.md) object.

```python
returnValue = applicationEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ApplicationEventHandler](ApplicationEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version January 2016  

