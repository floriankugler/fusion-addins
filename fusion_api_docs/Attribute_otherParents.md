# Attribute.otherParents Property

Parent Object: [Attribute](Attribute.md)  

## Description

In the case where the entity the attribute was originally placed on has been split, this property will return the other entities the attribute is associated with. For example, if an attribute is placed on a face and then a slot is created that cuts the face into two pieces and the attribute is available from both faces. The parent property returns the "primary" entity and this property returns any other entities, if any. If there aren't any other associated entities the ObjectCollection returned will be empty.

## Syntax

"attribute_var" is a variable referencing an Attribute object.  

```python
# Get the value of the property.
propertyValue = attribute_var.otherParents
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version January 2017  

