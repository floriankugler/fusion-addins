# Polyline3D.createByArray Method

Parent Object: [Polyline3D](Polyline3D.md)  

## Description

Creates a transient 3D polyline using an array of floating point values that specify the X, Y, Z coordinates for each point.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Polyline3D.createByArray(pointCoordinates)
```

## Return Value

| Type | Description |
|----|----|
| [Polyline3D](Polyline3D.md) | Returns the created Polyline3D object or null if the creation failed |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointCoordinates | double\[\] | An array of floating point values that define the X, Y, Z coordinates of each point in the polyline. |

## Version

Introduced in version September 2024  

