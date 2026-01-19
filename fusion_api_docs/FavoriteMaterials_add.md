# FavoriteMaterials.add Method

Parent Object: [FavoriteMaterials](FavoriteMaterials.md)  

## Description

Adds an existing material to the Favorites list

## Syntax

"favoriteMaterials_var" is a variable referencing a [FavoriteMaterials](FavoriteMaterials.md) object.

```python
returnValue = favoriteMaterials_var.add(material)
```

## Return Value

| Type | Description |
|----|----|
| [Material](Material.md) | Returns the Material added to the favorites list or null if the operation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| material | [Material](Material.md) | The material to be added to the favorites list. This can come from a Library or from a Design. |

## Version

Introduced in version January 2016  

