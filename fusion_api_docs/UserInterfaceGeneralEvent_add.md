# UserInterfaceGeneralEvent.add Method

Parent Object: [UserInterfaceGeneralEvent](UserInterfaceGeneralEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"userInterfaceGeneralEvent_var" is a variable referencing a [UserInterfaceGeneralEvent](UserInterfaceGeneralEvent.md) object.

```python
returnValue = userInterfaceGeneralEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [UserInterfaceGeneralEventHandler](UserInterfaceGeneralEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version March 2017  

