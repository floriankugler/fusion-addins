# Properties.itemByName Method

Parent Object: [Properties](Properties.md)  

## Description

Returns the specified Property using the name of the property.

## Syntax

"properties_var" is a variable referencing a [Properties](Properties.md) object.

```python
returnValue = properties_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Property](Property.md) | Returns the specified property or null if the name doesn't match a property within the collection. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the property to return. This is the name as seen in the user interface. |

## Version

Introduced in version August 2014  

