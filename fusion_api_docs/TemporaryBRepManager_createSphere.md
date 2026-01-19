# TemporaryBRepManager.createSphere Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a temporary spherical BRepBody object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createSphere(center, radius)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created temporary BRepBody object or null in the case of failure. |

## Parameters

| Name   | Type                   | Description                              |
|--------|------------------------|------------------------------------------|
| center | [Point3D](Point3D.md) | The center point of the sphere.          |
| radius | double                 | The radius of the sphere in centimeters. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

