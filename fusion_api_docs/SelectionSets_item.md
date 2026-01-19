# SelectionSets.item Method

Parent Object: [SelectionSets](SelectionSets.md)  

## Description

Returns the specified SelectionSet object using an index into the collection.

## Syntax

"selectionSets_var" is a variable referencing a [SelectionSets](SelectionSets.md) object.

```python
returnValue = selectionSets_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SelectionSet](SelectionSet.md) | Returns the specified SelectionSet or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the SelectionSet within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version May 2022  

