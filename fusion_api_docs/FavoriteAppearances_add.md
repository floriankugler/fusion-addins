# FavoriteAppearances.add Method

Parent Object: [FavoriteAppearances](FavoriteAppearances.md)  

## Description

Adds an existing appearance to the Favorites list

## Syntax

"favoriteAppearances_var" is a variable referencing a [FavoriteAppearances](FavoriteAppearances.md) object.

```python
returnValue = favoriteAppearances_var.add(appearance)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the Appearance added to the favorites list or null if the operation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| appearance | [Appearance](Appearance.md) | The appearance to be added to the favorites list. This can come from a Library or from a Design. |

## Version

Introduced in version January 2016  

