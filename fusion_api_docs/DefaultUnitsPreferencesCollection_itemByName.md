# DefaultUnitsPreferencesCollection.itemByName Method

Parent Object: [DefaultUnitsPreferencesCollection](DefaultUnitsPreferencesCollection.md)  

## Description

Returns the DefaultUnitsPreference object with the specified name.

## Syntax

"defaultUnitsPreferencesCollection_var" is a variable referencing a [DefaultUnitsPreferencesCollection](DefaultUnitsPreferencesCollection.md) object.

```python
returnValue = defaultUnitsPreferencesCollection_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [DefaultUnitsPreferences](DefaultUnitsPreferences.md) | Returns the DefaultUnitsPreference object or null if if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                       |
|------|--------|---------------------------------------------------|
| name | string | The name of the DefaultUnitsPreference to return. |

## Version

Introduced in version August 2014  

