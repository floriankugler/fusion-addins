# WorkspaceList.item Method

Parent Object: [WorkspaceList](WorkspaceList.md)  

## Description

Returns the specified work space using an index into the collection.

## Syntax

"workspaceList_var" is a variable referencing a [WorkspaceList](WorkspaceList.md) object.

```python
returnValue = workspaceList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Workspace](Workspace.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

