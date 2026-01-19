# Arc3D.createByCenter Method

Parent Object: [Arc3D](Arc3D.md)  

## Description

Creates a transient 3D arc object by specifying a center point and radius.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Arc3D.createByCenter(center, normal, referenceVector, radius, startAngle, endAngle)
```

## Return Value

| Type | Description |
|----|----|
| [Arc3D](Arc3D.md) | Returns the newly created arc or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the arc. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the arc. The plane perpendicular to this normal at the center point is the plane of the arc. |
| referenceVector | [Vector3D](Vector3D.md) | A reference vector from which the start and end angles are measured from. This vector must be perpendicular to the normal vector. |
| radius | double | The radius of the arc. |
| startAngle | double | The start angle in radians. This angle is measured from the reference vector using the right hand rule around the normal vector. |
| endAngle | double | The end angle in radians. This angle is measured from the reference vector using the right hand rule around the normal vector. |

## Version

Introduced in version August 2014  

