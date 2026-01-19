# Ellipse3D.set Method

Parent Object: [Ellipse3D](Ellipse3D.md)  

## Description

Sets all of the data defining the ellipse.

## Syntax

"ellipse3D_var" is a variable referencing an [Ellipse3D](Ellipse3D.md) object.

```python
returnValue = ellipse3D_var.set(center, normal, majorAxis, majorRadius, minorRadius)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The center point of the ellipse. |
| normal | [Vector3D](Vector3D.md) | The normal vector of the ellipse. The plane through the center point and perpendicular to the normal vector defines the plane of the ellipse. |
| majorAxis | [Vector3D](Vector3D.md) | The major axis of the ellipse. |
| majorRadius | double | The major radius of the of the ellipse. |
| minorRadius | double | The minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

