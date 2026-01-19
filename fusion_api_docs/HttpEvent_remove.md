# HttpEvent.remove Method

Parent Object: [HttpEvent](HttpEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"httpEvent_var" is a variable referencing a [HttpEvent](HttpEvent.md) object.

```python
returnValue = httpEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [HttpEventHandler](HttpEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version January 2024  

