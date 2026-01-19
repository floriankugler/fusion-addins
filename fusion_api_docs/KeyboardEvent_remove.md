# KeyboardEvent.remove Method

Parent Object: [KeyboardEvent](KeyboardEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"keyboardEvent_var" is a variable referencing a [KeyboardEvent](KeyboardEvent.md) object.

```python
returnValue = keyboardEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [KeyboardEventHandler](KeyboardEventHandler.md) | A KeyboardEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

