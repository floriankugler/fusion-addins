# Sketch.baseOrFormFeature Property

Parent Object: [Sketch](Sketch.md)  

## Description

This property returns the base or form feature that this sketch is associated with. It returns null in the case where the sketch is parametrically defined and is not related to a base or form feature. It also returns null in a direct modeling design.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.baseOrFormFeature
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version May 2016  

