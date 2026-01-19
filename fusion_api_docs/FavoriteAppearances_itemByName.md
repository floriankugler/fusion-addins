# FavoriteAppearances.itemByName Method

Parent Object: [FavoriteAppearances](FavoriteAppearances.md)  

## Description

Returns the specified appearance using the name as seen in the user interface. This often isn't a reliable way of accessing a specific appearance because appearances are not required to be unique.

## Syntax

"favoriteAppearances_var" is a variable referencing a [FavoriteAppearances](FavoriteAppearances.md) object.

```python
returnValue = favoriteAppearances_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the specified appearance or null if there isn't a matching name. |

## Parameters

| Name | Type   | Description                            |
|------|--------|----------------------------------------|
| name | string | The name of the appearance to return,. |

## Version

Introduced in version August 2014  

