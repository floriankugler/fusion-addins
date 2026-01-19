# ValidateInputsEvent.remove Method

Parent Object: [ValidateInputsEvent](ValidateInputsEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"validateInputsEvent_var" is a variable referencing a [ValidateInputsEvent](ValidateInputsEvent.md) object.

```python
returnValue = validateInputsEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ValidateInputsEventHandler](ValidateInputsEventHandler.md) | A ValidateInputsEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version August 2014  

