# WorkspaceList.itemById Method

Parent Object: [WorkspaceList](WorkspaceList.md)  

## Description

Returns the Workspace of the specified ID.

## Syntax

"workspaceList_var" is a variable referencing a [WorkspaceList](WorkspaceList.md) object.

```python
returnValue = workspaceList_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Workspace](Workspace.md) | Returns the specified workspace or null in the case where there isn't a workspace with the specified ID. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The ID of the workspace to get. |

## Version

Introduced in version August 2014  

