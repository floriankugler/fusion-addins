# SketchEllipticalArc.split Method

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Split a curve at a position specified along the curve

## Syntax

"sketchEllipticalArc_var" is a variable referencing a [SketchEllipticalArc](SketchEllipticalArc.md) object.

```python
# Uses no optional arguments.
returnValue = sketchEllipticalArc_var.split(splitPoint)

# Uses optional arguments.
returnValue = sketchEllipticalArc_var.split(splitPoint, createConstraints)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns the resulting 2 curves; the orginal curve + the newly created curve When split spline the original is deleted and two new curves returned. Empty collection returned if curve is closed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| splitPoint | [Point3D](Point3D.md) | A position (transient Point3D) on the curve that defines the point at which to split the curve |
| createConstraints | boolean | Constraints are created by default. Specify false to create no constraints. This is an optional argument whose default value is True. |

## Version

Introduced in version August 2014  

