# ToolbarTabList.item Method

Parent Object: [ToolbarTabList](ToolbarTabList.md)  

## Description

Returns the specified tab using an index into the collection.

## Syntax

"toolbarTabList_var" is a variable referencing a [ToolbarTabList](ToolbarTabList.md) object.

```python
returnValue = toolbarTabList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTab](ToolbarTab.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2019  

