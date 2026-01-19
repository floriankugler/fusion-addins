# FavoriteMaterials.itemById Method

Parent Object: [FavoriteMaterials](FavoriteMaterials.md)  

## Description

Returns the Material by it's internal unique ID.

## Syntax

"favoriteMaterials_var" is a variable referencing a [FavoriteMaterials](FavoriteMaterials.md) object.

```python
returnValue = favoriteMaterials_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the specified material or null if there isn't a matching ID. |

## Parameters

| Name | Type   | Description                       |
|------|--------|-----------------------------------|
| id   | string | The ID of the material to return. |

## Version

Introduced in version August 2014  

