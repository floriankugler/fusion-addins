# Sphere.create Method

Parent Object: [Sphere](Sphere.md)  

## Description

Creates a transient sphere object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Sphere.create(origin, radius)
```

## Return Value

| Type | Description |
|----|----|
| [Sphere](Sphere.md) | Returns the new Sphere object or null if the creation failed. |

## Parameters

| Name   | Type                   | Description                              |
|--------|------------------------|------------------------------------------|
| origin | [Point3D](Point3D.md) | The origin point (center) of the sphere. |
| radius | double                 | The radius of the sphere.                |

## Version

Introduced in version August 2014  

