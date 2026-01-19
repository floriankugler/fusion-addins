# Attribute.parent Property

Parent Object: [Attribute](Attribute.md)  

## Description

Returns the parent entity this attribute is associated with. This can return null in some cases. For example a BRepEdge might have been consumed by a fillet feature but can come back if the model is rolled back or the fillet is deleted.  

It's possible that the original parent that an attribute was placed on has been split. For example, if an attribute is placed on a face and then a slot is created that cuts the face into two pieces and the attribute is available from each face. In this case the parent property will return the "primary" face, which in most cases is somewhat arbitrary. You can get the other entities the attribute is associated with by using the otherParents property.

## Syntax

"attribute_var" is a variable referencing an Attribute object.  

```python
# Get the value of the property.
propertyValue = attribute_var.parent
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version May 2016  

