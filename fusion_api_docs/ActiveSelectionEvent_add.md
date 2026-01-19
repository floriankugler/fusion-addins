# ActiveSelectionEvent.add Method

Parent Object: [ActiveSelectionEvent](ActiveSelectionEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"activeSelectionEvent_var" is a variable referencing an [ActiveSelectionEvent](ActiveSelectionEvent.md) object.

```python
returnValue = activeSelectionEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ActiveSelectionEventHandler](ActiveSelectionEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version August 2020  

