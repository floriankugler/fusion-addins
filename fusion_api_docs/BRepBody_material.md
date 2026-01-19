# BRepBody.material Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Gets and sets the material assigned to this body.  

This property is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.material

# Set the value of the property.
bRepBody_var.material = propertyValue
```

## Property Value

This is a read/write property whose value is a [Material](Material.md).

## Version

Introduced in version August 2014  

