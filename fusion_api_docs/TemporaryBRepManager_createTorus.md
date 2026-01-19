# TemporaryBRepManager.createTorus Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a temporary toroidal BRepBody object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createTorus(center, axis, majorRadius, minorRadius)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created temporary BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the torus. |
| axis | [Vector3D](Vector3D.md) | The axis of the torus. |
| majorRadius | double | The radius, in centimeters, of the major radius of the torus. If the torus was created by sweeping a circle around another circle this would be the radius of the path circle. |
| minorRadius | double | The radius, in centimeters, of the minor radius of the torus. If the torus was created by sweeping a circle around another circle this would be the radius of the profile circle. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

