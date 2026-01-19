# Occurrences.item Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Function that returns the specified occurrence using an index into the collection.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

