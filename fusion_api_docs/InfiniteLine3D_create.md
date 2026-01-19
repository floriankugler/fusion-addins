# InfiniteLine3D.create Method

Parent Object: [InfiniteLine3D](InfiniteLine3D.md)  

## Description

Creates a transient 3D infinite line.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.InfiniteLine3D.create(origin, direction)
```

## Return Value

| Type | Description |
|----|----|
| [InfiniteLine3D](InfiniteLine3D.md) | Returns the new InfiniteLine3D object or null if the creation failed. |

## Parameters

| Name      | Type                     | Description                   |
|-----------|--------------------------|-------------------------------|
| origin    | [Point3D](Point3D.md)   | The origin point of the line. |
| direction | [Vector3D](Vector3D.md) | The direction of the line.    |

## Version

Introduced in version August 2014  

