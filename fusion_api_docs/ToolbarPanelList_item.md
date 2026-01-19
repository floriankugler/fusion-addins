# ToolbarPanelList.item Method

Parent Object: [ToolbarPanelList](ToolbarPanelList.md)  

## Description

Returns the specified work space using an index into the collection.

## Syntax

"toolbarPanelList_var" is a variable referencing a [ToolbarPanelList](ToolbarPanelList.md) object.

```python
returnValue = toolbarPanelList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarPanel](ToolbarPanel.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

