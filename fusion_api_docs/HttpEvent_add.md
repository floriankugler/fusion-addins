# HttpEvent.add Method

Parent Object: [HttpEvent](HttpEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"httpEvent_var" is a variable referencing a [HttpEvent](HttpEvent.md) object.

```python
returnValue = httpEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [HttpEventHandler](HttpEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version January 2024  

