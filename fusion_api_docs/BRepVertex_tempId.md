# BRepVertex.tempId Property

Parent Object: [BRepVertex](BRepVertex.md)  

## Description

Returns the temporary ID of this vertex. This ID is only good while the document remains open and as long as the owning BRepBody is not modified in any way. The findByTempId method of the BRepBody will return the entity in the body with the given ID.

## Syntax

"bRepVertex_var" is a variable referencing a BRepVertex object.  

```python
# Get the value of the property.
propertyValue = bRepVertex_var.tempId
```

## Property Value

This is a read only property whose value is an integer.

## Version

Introduced in version August 2016  

