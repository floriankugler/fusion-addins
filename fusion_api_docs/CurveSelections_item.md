# CurveSelections.item Method

Parent Object: [CurveSelections](CurveSelections.md)  

## Description

Function that returns the specified curve selection object using an index into the collection.

## Syntax

"curveSelections_var" is a variable referencing a [CurveSelections](CurveSelections.md) object.

```python
returnValue = curveSelections_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CurveSelection](CurveSelection.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version April 2023  

