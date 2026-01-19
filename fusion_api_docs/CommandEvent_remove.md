# CommandEvent.remove Method

Parent Object: [CommandEvent](CommandEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"commandEvent_var" is a variable referencing a [CommandEvent](CommandEvent.md) object.

```python
returnValue = commandEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CommandEventHandler](CommandEventHandler.md) | A CommandEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

