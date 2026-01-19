# Matrix3D.getAsCoordinateSystem Method

Parent Object: [Matrix3D](Matrix3D.md)  

## Description

Gets the matrix data as the components that define a coordinate system.

## Syntax

"matrix3D_var" is a variable referencing a [Matrix3D](Matrix3D.md) object.  

```python
(origin, xAxis, yAxis, zAxis) = matrix3D_var.getAsCoordinateSystem()
```

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point of the coordinate system. |
| xAxis | [Vector3D](Vector3D.md) | The output x axis direction of the coordinate system. |
| yAxis | [Vector3D](Vector3D.md) | The output y axis direction of the coordinate system. |
| zAxis | [Vector3D](Vector3D.md) | The output z axis direction of the coordinate system. |

## Version

Introduced in version August 2014  

