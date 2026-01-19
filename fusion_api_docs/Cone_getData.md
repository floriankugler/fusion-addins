# Cone.getData Method

Parent Object: [Cone](Cone.md)  

## Description

Gets the data that defines the cone.

## Syntax

"cone_var" is a variable referencing a [Cone](Cone.md) object.  

```python
(returnValue, origin, axis, radius, halfAngle) = cone_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point (center) of the base of the cone. |
| axis | [Vector3D](Vector3D.md) | The output center axis (along the length) of the cone that defines its normal direction. |
| radius | double | The output radius of the cone. |
| halfAngle | double | The output taper half-angle of the cone. |

## Version

Introduced in version August 2014  

