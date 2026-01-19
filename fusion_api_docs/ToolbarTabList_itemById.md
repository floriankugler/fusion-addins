# ToolbarTabList.itemById Method

Parent Object: [ToolbarTabList](ToolbarTabList.md)  

## Description

Returns the ToolbarTab of the specified ID.

## Syntax

"toolbarTabList_var" is a variable referencing a [ToolbarTabList](ToolbarTabList.md) object.

```python
returnValue = toolbarTabList_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTab](ToolbarTab.md) | Returns the specified ToolbarTab or null in the case where there isn't a ToolbarTab with the specified ID. |

## Parameters

| Name | Type   | Description                      |
|------|--------|----------------------------------|
| id   | string | The ID of the ToolbarTab to get. |

## Version

Introduced in version August 2019  

