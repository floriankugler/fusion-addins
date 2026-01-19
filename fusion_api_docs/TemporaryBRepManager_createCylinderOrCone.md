# TemporaryBRepManager.createCylinderOrCone Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a temporary solid cylinder or cone BRepBody object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createCylinderOrCone(pointOne, pointOneRadius, pointTwo, pointTwoRadius)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created temporary BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Point3D](Point3D.md) | A point at one end of the cylinder or cone. |
| pointOneRadius | double | The radius of the cylinder or cone at the point one end, in centimeters. |
| pointTwo | [Point3D](Point3D.md) | A point at the opposite end of the cylinder or cone. |
| pointTwoRadius | double | The radius of the cylinder or cone at the point two end, in centimeters. For a cylinder the pointTwoRadius should be equal to the pointOneRadius. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

