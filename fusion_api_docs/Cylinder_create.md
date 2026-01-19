# Cylinder.create Method

Parent Object: [Cylinder](Cylinder.md)  

## Description

Creates a transient cylinder object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Cylinder.create(origin, axis, radius)
```

## Return Value

| Type | Description |
|----|----|
| [Cylinder](Cylinder.md) | Returns the new Cylinder object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the base of the cylinder. |
| axis | [Vector3D](Vector3D.md) | The center axis (along the length) of the cylinder that defines its normal direction. |
| radius | double | The radius of the cylinder. |

## Version

Introduced in version August 2014  

