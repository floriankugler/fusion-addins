# Palettes.item Method

Parent Object: [Palettes](Palettes.md)  

## Description

Returns the specified palette using an index into the collection.

## Syntax

"palettes_var" is a variable referencing a [Palettes](Palettes.md) object.

```python
returnValue = palettes_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Palette](Palette.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2017  

