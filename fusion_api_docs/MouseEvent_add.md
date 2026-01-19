# MouseEvent.add Method

Parent Object: [MouseEvent](MouseEvent.md)  

## Description

Adds an event handler to this event endpoint.

## Syntax

"mouseEvent_var" is a variable referencing a [MouseEvent](MouseEvent.md) object.

```python
returnValue = mouseEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [MouseEventHandler](MouseEventHandler.md) | The client implemented MouseEventHandler to be called when this event is triggered. |

## Version

Introduced in version August 2014  

