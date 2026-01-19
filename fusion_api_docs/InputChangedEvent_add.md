# InputChangedEvent.add Method

Parent Object: [InputChangedEvent](InputChangedEvent.md)  

## Description

Adds an event handler to this event endpoint.

## Syntax

"inputChangedEvent_var" is a variable referencing an [InputChangedEvent](InputChangedEvent.md) object.

```python
returnValue = inputChangedEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [InputChangedEventHandler](InputChangedEventHandler.md) | The client implemented InputChangedEventHandler to be called when this event is triggered. |

## Version

Introduced in version August 2014  

