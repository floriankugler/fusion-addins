# PatternElements.item Method

Parent Object: [PatternElements](PatternElements.md)  

## Description

Function that returns the specified pattern element using an index into the collection.

## Syntax

"patternElements_var" is a variable referencing a [PatternElements](PatternElements.md) object.

```python
returnValue = patternElements_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [PatternElement](PatternElement.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

