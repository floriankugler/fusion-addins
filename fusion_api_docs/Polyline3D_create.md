# Polyline3D.create Method

Parent Object: [Polyline3D](Polyline3D.md)  

## Description

Creates a transient 3D polyline using an array of Point3D objects that defines the position of the polyline vertices.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Polyline3D.create(points)
```

## Return Value

| Type | Description |
|----|----|
| [Polyline3D](Polyline3D.md) | Returns the created Polyline3D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| points | Point3D\[\] | An array of Point3D objects that define the coordinates of the curve. |

## Version

Introduced in version September 2024  

