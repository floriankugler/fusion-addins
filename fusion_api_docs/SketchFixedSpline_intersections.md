# SketchFixedSpline.intersections Method

Parent Object: [SketchFixedSpline](SketchFixedSpline.md)  

## Description

Get the curves that intersect this curve along with the intersection points (Point3D)

## Syntax

"sketchFixedSpline_var" is a variable referencing a [SketchFixedSpline](SketchFixedSpline.md) object.  

```python
(returnValue, intersectingCurves, intersectionPoints) = sketchFixedSpline_var.intersections(sketchCurves)
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns true if intersections are found |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchCurves | [ObjectCollection](ObjectCollection.md) | A collection of curves to attempt to find intersections with. Set the value of this parameter to null to use all curves in the sketch for the calculation. |
| intersectingCurves | [ObjectCollection](ObjectCollection.md) | A collection of the actual intersecting curves |
| intersectionPoints | [ObjectCollection](ObjectCollection.md) | A collection of intersection points (Point3D) Item numbers in this collection correspond to the item numbers in the intersectingCurves collection. |

## Version

Introduced in version August 2014  

