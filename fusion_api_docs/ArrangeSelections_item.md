# ArrangeSelections.item Method

Parent Object: [ArrangeSelections](ArrangeSelections.md)  

## Description

Function that returns the specified arrange selection object using an index into the collection.

## Syntax

"arrangeSelections_var" is a variable referencing an [ArrangeSelections](ArrangeSelections.md) object.

```python
returnValue = arrangeSelections_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ArrangeSelection](ArrangeSelection.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2024  

