# Cone.set Method

Parent Object: [Cone](Cone.md)  

## Description

Sets the data that defines the cone.

## Syntax

"cone_var" is a variable referencing a [Cone](Cone.md) object.

```python
returnValue = cone_var.set(origin, axis, radius, halfAngle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cone. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cone that defines its normal direction. |
| radius | double | The radius of the cone. |
| halfAngle | double | The taper half-angle of the cone. |

## Version

Introduced in version August 2014  

