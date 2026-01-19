# DocumentEvent.add Method

Parent Object: [DocumentEvent](DocumentEvent.md)  

## Description

Add a handler to be notified when the file event occurs.

## Syntax

"documentEvent_var" is a variable referencing a [DocumentEvent](DocumentEvent.md) object.

```python
returnValue = documentEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [DocumentEventHandler](DocumentEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version August 2014  

