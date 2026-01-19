# SketchConicCurve.referencedEntity Property

Parent Object: [SketchConicCurve](SketchConicCurve.md)  

## Description

Returns the referenced entity in the case where IsReference is true. However, this property can also return null when IsReference is true in the case where the reference is not parametric.

## Syntax

"sketchConicCurve_var" is a variable referencing a SketchConicCurve object.  

```python
# Get the value of the property.
propertyValue = sketchConicCurve_var.referencedEntity
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2015  

