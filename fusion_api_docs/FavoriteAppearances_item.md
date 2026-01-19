# FavoriteAppearances.item Method

Parent Object: [FavoriteAppearances](FavoriteAppearances.md)  

## Description

Returns the specified Appearance using an index into the collection.

## Syntax

"favoriteAppearances_var" is a variable referencing a [FavoriteAppearances](FavoriteAppearances.md) object.

```python
returnValue = favoriteAppearances_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the specified appearance or null if an invalid index is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the appearance to return where the first item in the collection is 0. |

## Version

Introduced in version August 2014  

