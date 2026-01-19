# ProductPreferencesCollection.item Method

Parent Object: [ProductPreferencesCollection](ProductPreferencesCollection.md)  

## Description

Function that returns the specified ProductPreferences object using an index into the collection.

## Syntax

"productPreferencesCollection_var" is a variable referencing a [ProductPreferencesCollection](ProductPreferencesCollection.md) object.

```python
returnValue = productPreferencesCollection_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ProductPreferences](ProductPreferences.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

