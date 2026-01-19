# BRepFace.isPointOnFace Method

Parent Object: [BRepFace](BRepFace.md)  

## Description

Checks if input point is on this BRepFace. This takes into account any boundaries so if the point is within a void area of the face, this will return false.

## Syntax

"bRepFace_var" is a variable referencing a [BRepFace](BRepFace.md) object.

```python
# Uses no optional arguments.
returnValue = bRepFace_var.isPointOnFace(point)

# Uses optional arguments.
returnValue = bRepFace_var.isPointOnFace(point, tolerance)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true if the point lies on the face. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| point | [Point3D](Point3D.md) | The input point to check. |
| tolerance | double | Specifies how close the point must be to the face to be considered on the face. Defaults to the point tolerance which can be obtained using the Application.pointTolerance property. The value is in centimeters. This is an optional argument whose default value is 0.0. |

## Version

Introduced in version September 2024  

