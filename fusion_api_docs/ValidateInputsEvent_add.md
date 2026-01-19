# ValidateInputsEvent.add Method

Parent Object: [ValidateInputsEvent](ValidateInputsEvent.md)  

## Description

Adds an event handler to this event endpoint.

## Syntax

"validateInputsEvent_var" is a variable referencing a [ValidateInputsEvent](ValidateInputsEvent.md) object.

```python
returnValue = validateInputsEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ValidateInputsEventHandler](ValidateInputsEventHandler.md) | The client implemented ValidateInputsEventHandler to be called when this event is triggered. |

## Version

Introduced in version August 2014  

