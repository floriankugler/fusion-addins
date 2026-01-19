# InputChangedEvent.remove Method

Parent Object: [InputChangedEvent](InputChangedEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"inputChangedEvent_var" is a variable referencing an [InputChangedEvent](InputChangedEvent.md) object.

```python
returnValue = inputChangedEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [InputChangedEventHandler](InputChangedEventHandler.md) | A InputChangedEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

