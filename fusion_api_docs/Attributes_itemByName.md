# Attributes.itemByName Method

Parent Object: [Attributes](Attributes.md)  

## Description

Returns the specified attribute using the name of the attribute.

## Syntax

"attributes_var" is a variable referencing an [Attributes](Attributes.md) object.

```python
returnValue = attributes_var.itemByName(groupName, name)
```

## Return Value

| Type | Description |
|----|----|
| [Attribute](Attribute.md) | Returns the specified attribute or null if no attribute exists with the specified name. |

## Parameters

| Name | Type | Description |
|----|----|----|
| groupName | string | The name of the attribute group this attribute will belong to. |
| name | string | The name of the attribute. |

## Version

Introduced in version May 2016  

