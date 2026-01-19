# SelectionEvent.remove Method

Parent Object: [SelectionEvent](SelectionEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"selectionEvent_var" is a variable referencing a [SelectionEvent](SelectionEvent.md) object.

```python
returnValue = selectionEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SelectionEventHandler](SelectionEventHandler.md) | A SelectionEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

