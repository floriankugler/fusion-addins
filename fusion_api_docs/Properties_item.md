# Properties.item Method

Parent Object: [Properties](Properties.md)  

## Description

Returns the specified property from the collection using an index into the collection.

## Syntax

"properties_var" is a variable referencing a [Properties](Properties.md) object.

```python
returnValue = properties_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Property](Property.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the property within the collection where the first item is 0. |

## Version

Introduced in version August 2014  

