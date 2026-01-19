# SketchArc.geometry Property

Parent Object: [SketchArc](SketchArc.md)  

## Description

Returns the transient geometry of the arc which provides geometric information about the arc. The returned geometry is always in sketch space.

## Syntax

"sketchArc_var" is a variable referencing a SketchArc object.  

```python
# Get the value of the property.
propertyValue = sketchArc_var.geometry
```

## Property Value

This is a read only property whose value is an [Arc3D](Arc3D.md).

## Samples

| Name | Description |
|----|----|
| [SketchArcs.split](SketchArcs_split_Sample.md) | Demonstrates the SketchArc.split method. |

## Version

Introduced in version August 2014  

