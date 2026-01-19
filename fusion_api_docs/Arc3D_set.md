# Arc3D.set Method

Parent Object: [Arc3D](Arc3D.md)  

## Description

Sets all of the data defining the arc.

## Syntax

"arc3D_var" is a variable referencing an [Arc3D](Arc3D.md) object.

```python
returnValue = arc3D_var.set(center, normal, referenceVector, radius, startAngle, endAngle)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

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

