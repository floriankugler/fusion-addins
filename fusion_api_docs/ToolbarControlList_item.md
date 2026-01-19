# ToolbarControlList.item Method

Parent Object: [ToolbarControlList](ToolbarControlList.md)  

## Description

Returns the ToolbarControl at the specified index. When iterating by index, the controls are returned in the same order as they are shown in the user interface.

## Syntax

"toolbarControlList_var" is a variable referencing a [ToolbarControlList](ToolbarControlList.md) object.

```python
returnValue = toolbarControlList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarControl](ToolbarControl.md) | Returns the ToolbarControl at the specified index or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the control within the collection to return. The first item in the collection has in index of 0. |

## Version

Introduced in version August 2014  

