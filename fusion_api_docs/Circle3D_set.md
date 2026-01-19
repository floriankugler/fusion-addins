# Circle3D.set Method

Parent Object: [Circle3D](Circle3D.md)  

## Description

Sets all of the data defining the circle.

## Syntax

"circle3D_var" is a variable referencing a [Circle3D](Circle3D.md) object.

```python
returnValue = circle3D_var.set(center, normal, radius)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the circle. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the circle. The plane through the center point and perpendicular to the normal vector defines the plane of the circle. |
| radius | double | The radius of the circle. |

## Version

Introduced in version August 2014  

