# DocumentEvent.remove Method

Parent Object: [DocumentEvent](DocumentEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"documentEvent_var" is a variable referencing a [DocumentEvent](DocumentEvent.md) object.

```python
returnValue = documentEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [DocumentEventHandler](DocumentEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version August 2014  

