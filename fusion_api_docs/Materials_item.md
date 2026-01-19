# Materials.item Method

Parent Object: [Materials](Materials.md)  

## Description

Returns the specified Material using an index into the collection.

## Syntax

"materials_var" is a variable referencing a [Materials](Materials.md) object.

```python
returnValue = materials_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the specified material or null if an invalid index is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the material to return where the first item in the collection is 0. |

## Version

Introduced in version August 2014  

