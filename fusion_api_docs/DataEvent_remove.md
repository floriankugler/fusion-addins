# DataEvent.remove Method

Parent Object: [DataEvent](DataEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"dataEvent_var" is a variable referencing a [DataEvent](DataEvent.md) object.

```python
returnValue = dataEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [DataEventHandler](DataEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version January 2022  

