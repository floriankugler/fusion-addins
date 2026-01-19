# SelectionEvent.add Method

Parent Object: [SelectionEvent](SelectionEvent.md)  

## Description

Adds an event handler to this event endpoint.

## Syntax

"selectionEvent_var" is a variable referencing a [SelectionEvent](SelectionEvent.md) object.

```python
returnValue = selectionEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SelectionEventHandler](SelectionEventHandler.md) | The client implemented SelectionEventHandler to be called when this event is triggered. |

## Version

Introduced in version August 2014  

