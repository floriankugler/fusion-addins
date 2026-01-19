# ListItems.item Method

Parent Object: [ListItems](ListItems.md)  

## Description

Returns the specified check box list item using an index into the collection.

## Syntax

"listItems_var" is a variable referencing a [ListItems](ListItems.md) object.

```python
returnValue = listItems_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ListItem](ListItem.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2015  

