# CustomEvent.remove Method

Parent Object: [CustomEvent](CustomEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"customEvent_var" is a variable referencing a [CustomEvent](CustomEvent.md) object.

```python
returnValue = customEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CustomEventHandler](CustomEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version January 2017  

