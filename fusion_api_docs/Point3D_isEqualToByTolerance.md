# Point3D.isEqualToByTolerance Method

Parent Object: [Point3D](Point3D.md)  

## Description

Checks to see if this point and another point are equal within the specified tolerance.

## Syntax

"point3D_var" is a variable referencing a [Point3D](Point3D.md) object.

```python
returnValue = point3D_var.isEqualToByTolerance(point, tolerance)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the points are equal (have identical coordinates). |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point3D](Point3D.md) | The point to compare for equality. |
| tolerance | double | The tolerance, in centimeters, to use when comparing the two points. |

## Version

Introduced in version December 2017  

