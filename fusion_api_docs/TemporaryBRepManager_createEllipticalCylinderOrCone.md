# TemporaryBRepManager.createEllipticalCylinderOrCone Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a temporary elliptical solid cylinder or cone BrepBody object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createEllipticalCylinderOrCone(pointOne, pointOneMajorRadius, pointOneMinorRadius, pointTwo, pointTwoMajorRadius, majorAxisDirection)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created temporary BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Point3D](Point3D.md) | A point at one end of the cylinder or cone. |
| pointOneMajorRadius | double | The major radius of the cylinder or cone at the point one end, in centimeters. |
| pointOneMinorRadius | double | The minor radius of the cylinder or cone at the point one end, in centimeters. |
| pointTwo | [Point3D](Point3D.md) | A point at the opposite end of the cone. |
| pointTwoMajorRadius | double | The major radius of the cylinder or cone at the point two end, in centimeters. The minor radius is automatically determined using the point one ratio of the minor and major radii. |
| majorAxisDirection | [Vector3D](Vector3D.md) | A Vector3D object that defines the direction of the major axis. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

