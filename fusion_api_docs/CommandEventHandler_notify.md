# CommandEventHandler.notify Method

Parent Object: [CommandEventHandler](CommandEventHandler.md)  

## Description

This notify member is called when an event is triggered from any event that this handler has been added to.

## Syntax

"commandEventHandler_var" is a variable referencing a [CommandEventHandler](CommandEventHandler.md) object.

```python
returnValue = commandEventHandler_var.notify(eventArgs)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| eventArgs | [CommandEventArgs](CommandEventArgs.md) | The arguments object with details about this event and the firing CommandEvent. |

## Version

Introduced in version August 2014  

