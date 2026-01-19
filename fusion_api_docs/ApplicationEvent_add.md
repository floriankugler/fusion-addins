# ApplicationEvent.add Method

Parent Object: [ApplicationEvent](ApplicationEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"applicationEvent_var" is a variable referencing an [ApplicationEvent](ApplicationEvent.md) object.

```python
returnValue = applicationEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ApplicationEventHandler](ApplicationEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version January 2016  

