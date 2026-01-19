# ToolbarPanels.item Method

Parent Object: [ToolbarPanels](ToolbarPanels.md)  

## Description

Returns the specified toolbar panel using an index into the collection. When iterating by index, the panels are returned in the same order as they are shown in the user interface.

## Syntax

"toolbarPanels_var" is a variable referencing a [ToolbarPanels](ToolbarPanels.md) object.

```python
returnValue = toolbarPanels_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarPanel](ToolbarPanel.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

