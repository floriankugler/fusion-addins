# ApplicationCommandEvent.remove Method

Parent Object: [ApplicationCommandEvent](ApplicationCommandEvent.md)  

## Description

Removes a handler from this event endpoint.

## Syntax

"applicationCommandEvent_var" is a variable referencing an [ApplicationCommandEvent](ApplicationCommandEvent.md) object.

```python
returnValue = applicationCommandEvent_var.remove(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was found and removed from the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ApplicationCommandEventHandler](ApplicationCommandEventHandler.md) | An ApplicationCommandEventHandler that was previously added to this event with the add method. |

## Version

Introduced in version November 2015  

