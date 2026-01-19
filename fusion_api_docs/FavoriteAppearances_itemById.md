# FavoriteAppearances.itemById Method

Parent Object: [FavoriteAppearances](FavoriteAppearances.md)  

## Description

Returns the Appearance by it's internal unique ID.

## Syntax

"favoriteAppearances_var" is a variable referencing a [FavoriteAppearances](FavoriteAppearances.md) object.

```python
returnValue = favoriteAppearances_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the specified appearance or null if there isn't a matching ID. |

## Parameters

| Name | Type   | Description                         |
|------|--------|-------------------------------------|
| id   | string | The ID of the appearance to return. |

## Version

Introduced in version August 2014  

