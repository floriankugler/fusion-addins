# CommandCreatedEventHandler.notify Method

Parent Object: [CommandCreatedEventHandler](CommandCreatedEventHandler.md)  

## Description

This notify member is called when an event is triggered from any event that this handler has been added to.

## Syntax

"commandCreatedEventHandler_var" is a variable referencing a [CommandCreatedEventHandler](CommandCreatedEventHandler.md) object.

```python
returnValue = commandCreatedEventHandler_var.notify(eventArgs)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| eventArgs | [CommandCreatedEventArgs](CommandCreatedEventArgs.md) | The arguments object with details about this event and the firing CommandEvent. |

## Version

Introduced in version August 2014  

