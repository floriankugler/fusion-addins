# CAMPatterns.item Method

Parent Object: [CAMPatterns](CAMPatterns.md)  

## Description

Function that returns the specified pattern using an index into the collection.

## Syntax

"cAMPatterns_var" is a variable referencing a [CAMPatterns](CAMPatterns.md) object.

```python
returnValue = cAMPatterns_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CAMPattern](CAMPattern.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2016  

