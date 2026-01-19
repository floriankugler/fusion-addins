# Matrix3D.setWithCoordinateSystem Method

Parent Object: [Matrix3D](Matrix3D.md)  

## Description

Sets the matrix based on the components of a coordinate system.

## Syntax

"matrix3D_var" is a variable referencing a [Matrix3D](Matrix3D.md) object.

```python
returnValue = matrix3D_var.setWithCoordinateSystem(origin, xAxis, yAxis, zAxis)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point of the coordinate system. |
| xAxis | [Vector3D](Vector3D.md) | The x axis direction of the coordinate system. |
| yAxis | [Vector3D](Vector3D.md) | The y axis direction of the coordinate system. |
| zAxis | [Vector3D](Vector3D.md) | The z axis direction of the coordinate system. |

## Version

Introduced in version August 2014  

