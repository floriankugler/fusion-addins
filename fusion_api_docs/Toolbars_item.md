# Toolbars.item Method

Parent Object: [Toolbars](Toolbars.md)  

## Description

Returns the specified toolbar using an index into the collection.

## Syntax

"toolbars_var" is a variable referencing a [Toolbars](Toolbars.md) object.

```python
returnValue = toolbars_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Toolbar](Toolbar.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

