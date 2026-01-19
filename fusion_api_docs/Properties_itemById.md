# Properties.itemById Method

Parent Object: [Properties](Properties.md)  

## Description

Returns the specified property from the collection using the unique ID of the property.

## Syntax

"properties_var" is a variable referencing a [Properties](Properties.md) object.

```python
returnValue = properties_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Property](Property.md) | Returns the specified property or null if the ID doesn't match a property within the collection. |

## Parameters

| Name | Type   | Description                    |
|------|--------|--------------------------------|
| id   | string | The unique ID of the property. |

## Version

Introduced in version August 2014  

