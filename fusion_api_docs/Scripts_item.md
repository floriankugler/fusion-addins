# Scripts.item Method

Parent Object: [Scripts](Scripts.md)  

## Description

Function that returns the specified script or add-in using an index into the collection.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Script](Script.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version October 2023  

