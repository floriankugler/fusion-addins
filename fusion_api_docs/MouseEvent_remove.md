# MouseEvent.remove Method

Parent Object: [MouseEvent](MouseEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"mouseEvent_var" is a variable referencing a [MouseEvent](MouseEvent.md) object.

```python
returnValue = mouseEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [MouseEventHandler](MouseEventHandler.md) | A MouseEventhandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

