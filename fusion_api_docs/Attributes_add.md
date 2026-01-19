# Attributes.add Method

Parent Object: [Attributes](Attributes.md)  

## Description

Adds a new attribute to the parent entity. If an attribute already exists on the entity with the same groupName and name already exists, this will update the existing attribute with the new value.

## Syntax

"attributes_var" is a variable referencing an [Attributes](Attributes.md) object.

```python
returnValue = attributes_var.add(groupName, name, value)
```

## Return Value

| Type | Description |
|----|----|
| [Attribute](Attribute.md) | Returns the newly created attribute or null if the creation failed. If an attribute with the same groupName and name already exists, it will return the existing attribute. |

## Parameters

| Name | Type | Description |
|----|----|----|
| groupName | string | The name of the attribute group to create this attribute within. |
| name | string | The name of the attribute. This must be unique with respect to other attributes in the group. |
| value | string | The value of the attribute. The size of an attribute value is limited to 2MB (2097152 bytes). If you need to save data that is larger than 2MB you'll need to break it into pieces and save it in multiple attributes. |

## Version

Introduced in version May 2016  

