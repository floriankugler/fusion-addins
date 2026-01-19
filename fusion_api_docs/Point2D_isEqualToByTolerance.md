# Point2D.isEqualToByTolerance Method

Parent Object: [Point2D](Point2D.md)  

## Description

Checks to see if this point and another point are equal within the specified tolerance.

## Syntax

"point2D_var" is a variable referencing a [Point2D](Point2D.md) object.

```python
returnValue = point2D_var.isEqualToByTolerance(point, tolerance)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the points are equal (have identical coordinates). |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point2D](Point2D.md) | The point to compare for equality. |
| tolerance | double | The tolerance, in centimeters, to use when comparing the two points. |

## Version

Introduced in version December 2017  

