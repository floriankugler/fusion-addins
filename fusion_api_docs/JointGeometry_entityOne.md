# JointGeometry.entityOne Property

Parent Object: [JointGeometry](JointGeometry.md)  

## Description

The first entity that's defining this joint geometry. This can be various types of geometry depending on how this joint geometry is defined. The geometryType property indicates how this joint geometry is defined a provides a clue about the type of geometry to expect back from this property.

## Syntax

"jointGeometry_var" is a variable referencing a JointGeometry object.  

```python
# Get the value of the property.
propertyValue = jointGeometry_var.entityOne
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

