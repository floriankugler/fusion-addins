# Selections.item Method

Parent Object: [Selections](Selections.md)  

## Description

Returns the specified selection using an index into the collection.

## Syntax

"selections_var" is a variable referencing a [Selections](Selections.md) object.

```python
returnValue = selections_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Selection](Selection.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

