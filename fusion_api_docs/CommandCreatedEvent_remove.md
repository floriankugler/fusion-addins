# CommandCreatedEvent.remove Method

Parent Object: [CommandCreatedEvent](CommandCreatedEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"commandCreatedEvent_var" is a variable referencing a [CommandCreatedEvent](CommandCreatedEvent.md) object.

```python
returnValue = commandCreatedEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CommandCreatedEventHandler](CommandCreatedEventHandler.md) | A CommandCreatedEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

