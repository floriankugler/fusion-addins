# SketchCurve.isLinked Property

Parent Object: [SketchCurve](SketchCurve.md)  

## Description

Indicates if this sketch entity was created by a projection, inclusion, or driven by an API script. If this returns true, then the entity is presented to the user as not editable and with a 'break link' command available.

## Syntax

"sketchCurve_var" is a variable referencing a SketchCurve object.  

```python
# Get the value of the property.
propertyValue = sketchCurve_var.isLinked
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version December 2020  

