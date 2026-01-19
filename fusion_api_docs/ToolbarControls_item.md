# ToolbarControls.item Method

Parent Object: [ToolbarControls](ToolbarControls.md)  

## Description

Returns the ToolbarControl at the specified index. When iterating by index, the controls are returned in the same order as they are shown in the user interface.

## Syntax

"toolbarControls_var" is a variable referencing a [ToolbarControls](ToolbarControls.md) object.

```python
returnValue = toolbarControls_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarControl](ToolbarControl.md) | Returns the ToolbarControl at the specified index or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the control within the collection to return. The first item in the collection has in index of 0. |

## Samples

| Name | Description |
|----|----|
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

