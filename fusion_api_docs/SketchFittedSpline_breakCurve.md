# SketchFittedSpline.breakCurve Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Breaks a curve into two or three pieces by finding intersections of this curve with all other curves in the sketch and splitting this curve at the nearest intersections to a specified point on the curve.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
# Uses no optional arguments.
returnValue = sketchFittedSpline_var.breakCurve(segmentPoint)

# Uses optional arguments.
returnValue = sketchFittedSpline_var.breakCurve(segmentPoint, createConstraints)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | All of the curves resulting from the break are returned in an ObjectCollection. In the case where no intersections are found and as a result the curve is not broken, an empty ObjectCollection is returned. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| segmentPoint | [Point3D](Point3D.md) | A point that specifies the segment of the curve that is to be split from the rest of the curve. The nearest intersection(s) to this point define the break location(s). |
| createConstraints | boolean | Optional argument that specifies if constraints should be created between the new curve segments. A value of true indicates constraints will be created. This is an optional argument whose default value is True. |

## Version

Introduced in version August 2014  

