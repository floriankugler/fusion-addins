# ToolbarTabs.item Method

Parent Object: [ToolbarTabs](ToolbarTabs.md)  

## Description

Returns the specified toolbar tab using an index into the collection. When iterating by index, the tabs are returned in the same order as they are shown in the user interface.

## Syntax

"toolbarTabs_var" is a variable referencing a [ToolbarTabs](ToolbarTabs.md) object.

```python
returnValue = toolbarTabs_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTab](ToolbarTab.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
|----|----|
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2019  

