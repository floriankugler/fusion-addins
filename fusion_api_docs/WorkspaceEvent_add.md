# WorkspaceEvent.add Method

Parent Object: [WorkspaceEvent](WorkspaceEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"workspaceEvent_var" is a variable referencing a [WorkspaceEvent](WorkspaceEvent.md) object.

```python
returnValue = workspaceEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [WorkspaceEventHandler](WorkspaceEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version March 2015  

