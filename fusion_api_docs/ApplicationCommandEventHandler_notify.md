# ApplicationCommandEventHandler.notify Method

Parent Object: [ApplicationCommandEventHandler](ApplicationCommandEventHandler.md)  

## Description

This notify member is called when an event is triggered from any event that this handler has been added to.

## Syntax

"applicationCommandEventHandler_var" is a variable referencing an [ApplicationCommandEventHandler](ApplicationCommandEventHandler.md) object.

```python
returnValue = applicationCommandEventHandler_var.notify(eventArgs)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| eventArgs | [ApplicationCommandEventArgs](ApplicationCommandEventArgs.md) | The arguments object with details about this event and the firing ApplicationCommandEvent. |

## Version

Introduced in version November 2015  

