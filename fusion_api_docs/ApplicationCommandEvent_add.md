# ApplicationCommandEvent.add Method

Parent Object: [ApplicationCommandEvent](ApplicationCommandEvent.md)  

## Description

Adds an event handler object to this event endpoint.

## Syntax

"applicationCommandEvent_var" is a variable referencing an [ApplicationCommandEvent](ApplicationCommandEvent.md) object.

```python
returnValue = applicationCommandEvent_var.add(handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the handler was successfully added to the set of event handlers. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [ApplicationCommandEventHandler](ApplicationCommandEventHandler.md) | The ApplicationCommandEventHandler to be called when this event is triggered. |

## Version

Introduced in version November 2015  

