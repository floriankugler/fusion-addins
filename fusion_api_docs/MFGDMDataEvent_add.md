# MFGDMDataEvent.add Method

Parent Object: [MFGDMDataEvent](MFGDMDataEvent.md)  

## Description

Add a handler to be notified when the data event occurs.

## Syntax

"mFGDMDataEvent_var" is a variable referencing a [MFGDMDataEvent](MFGDMDataEvent.md) object.

```python
returnValue = mFGDMDataEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [MFGDMDataEventHandler](MFGDMDataEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version July 2025  

