# ProductPreferencesCollection.itemByName Method

Parent Object: [ProductPreferencesCollection](ProductPreferencesCollection.md)  

## Description

Returns the ProductPreference object with the specified name.

## Syntax

"productPreferencesCollection_var" is a variable referencing a [ProductPreferencesCollection](ProductPreferencesCollection.md) object.

```python
returnValue = productPreferencesCollection_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ProductPreferences](ProductPreferences.md) | Returns the ProductPreferences object or null if if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                   |
|------|--------|-----------------------------------------------|
| name | string | The name of the ProductPreferences to return. |

## Version

Introduced in version August 2014  

