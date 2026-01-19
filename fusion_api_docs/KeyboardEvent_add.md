# KeyboardEvent.add Method

Parent Object: [KeyboardEvent](KeyboardEvent.md)  

## Description

Adds an event handler to this event endpoint.

## Syntax

"keyboardEvent_var" is a variable referencing a [KeyboardEvent](KeyboardEvent.md) object.

```python
returnValue = keyboardEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [KeyboardEventHandler](KeyboardEventHandler.md) | The client implemented KeyboardEventHandler to be called when this event is triggered. |

## Version

Introduced in version August 2014  

