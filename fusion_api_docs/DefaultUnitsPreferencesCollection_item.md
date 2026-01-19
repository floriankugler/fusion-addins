# DefaultUnitsPreferencesCollection.item Method

Parent Object: [DefaultUnitsPreferencesCollection](DefaultUnitsPreferencesCollection.md)  

## Description

Function that returns the specified DefaultUnitPreferences object using an index into the collection.

## Syntax

"defaultUnitsPreferencesCollection_var" is a variable referencing a [DefaultUnitsPreferencesCollection](DefaultUnitsPreferencesCollection.md) object.

```python
returnValue = defaultUnitsPreferencesCollection_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DefaultUnitsPreferences](DefaultUnitsPreferences.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

