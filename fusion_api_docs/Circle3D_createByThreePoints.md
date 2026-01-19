# Circle3D.createByThreePoints Method

Parent Object: [Circle3D](Circle3D.md)  

## Description

Creates a transient 3D circle through three points.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Circle3D.createByThreePoints(pointOne, pointTwo, pointThree)
```

## Return Value

| Type | Description |
|----|----|
| [Circle3D](Circle3D.md) | Returns the new Circle3D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Point3D](Point3D.md) | The first point on the circle. |
| pointTwo | [Point3D](Point3D.md) | The second point on the circle. This point cannot be coincident with pointOne or pointThree. This point cannot lie on the line defined by pointOne and pointThree. |
| pointThree | [Point3D](Point3D.md) | The third point on the circle. This point cannot be coincident with pointOne or pointThree. |

## Version

Introduced in version August 2014  

