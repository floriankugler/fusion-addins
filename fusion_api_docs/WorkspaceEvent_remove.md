# WorkspaceEvent.remove Method

Parent Object: [WorkspaceEvent](WorkspaceEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"workspaceEvent_var" is a variable referencing a [WorkspaceEvent](WorkspaceEvent.md) object.

```python
returnValue = workspaceEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [WorkspaceEventHandler](WorkspaceEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version March 2015  

