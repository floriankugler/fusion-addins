# SketchEllipticalArc.isLinked Property

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Indicates if this sketch entity was created by a projection, inclusion, or driven by an API script. If this returns true, then the entity is presented to the user as not editable and with a 'break link' command available.

## Syntax

"sketchEllipticalArc_var" is a variable referencing a SketchEllipticalArc object.  

```python
# Get the value of the property.
propertyValue = sketchEllipticalArc_var.isLinked
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version December 2020  

