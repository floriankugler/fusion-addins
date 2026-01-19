# InterferenceResults.item Method

Parent Object: [InterferenceResults](InterferenceResults.md)  

## Description

Function that returns the specified interference result using an index into the collection.

## Syntax

"interferenceResults_var" is a variable referencing an [InterferenceResults](InterferenceResults.md) object.

```python
returnValue = interferenceResults_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [InterferenceResult](InterferenceResult.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2015  

