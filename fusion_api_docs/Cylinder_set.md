# Cylinder.set Method

Parent Object: [Cylinder](Cylinder.md)  

## Description

Sets the data that defines the cylinder.

## Syntax

"cylinder_var" is a variable referencing a [Cylinder](Cylinder.md) object.

```python
returnValue = cylinder_var.set(origin, axis, radius)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cylinder. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cylinder that defines its normal direction. |
| radius | double | The radius of the cylinder. |

## Version

Introduced in version August 2014  

