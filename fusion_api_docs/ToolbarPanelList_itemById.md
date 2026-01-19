# ToolbarPanelList.itemById Method

Parent Object: [ToolbarPanelList](ToolbarPanelList.md)  

## Description

Returns the ToolbarPanel of the specified ID.

## Syntax

"toolbarPanelList_var" is a variable referencing a [ToolbarPanelList](ToolbarPanelList.md) object.

```python
returnValue = toolbarPanelList_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarPanel](ToolbarPanel.md) | Returns the specified ToolbarPanel or null in the case where there isn't a ToolbarPanel with the specified ID. |

## Parameters

| Name | Type   | Description                        |
|------|--------|------------------------------------|
| id   | string | The ID of the ToolbarPanel to get. |

## Version

Introduced in version June 2015  

