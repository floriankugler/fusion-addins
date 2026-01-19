# Attributes.itemsByGroup Method

Parent Object: [Attributes](Attributes.md)  

## Description

Returns an array of all of the attributes that belong to the specified group.

## Syntax

"attributes_var" is a variable referencing an [Attributes](Attributes.md) object.

```python
returnValue = attributes_var.itemsByGroup(groupName)
```

## Return Value

| Type | Description |
|----|----|
| [Attribute](Attribute.md)\[\] | Returns an array of attributes or will fail in the case where an invalid group name is specified. |

## Parameters

| Name      | Type   | Description            |
|-----------|--------|------------------------|
| groupName | string | The name of the group. |

## Version

Introduced in version May 2016  

