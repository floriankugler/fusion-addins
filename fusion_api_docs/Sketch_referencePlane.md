# Sketch.referencePlane Property

Parent Object: [Sketch](Sketch.md)  

## Description

Gets and sets the construction plane or planar face the sketch is associated to. This is only valid when the IsParametric property is True otherwise this returns null and setting the property will fail.  

Setting this property is the equivalent of the Redefine command.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.referencePlane

# Set the value of the property.
sketch_var.referencePlane = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

