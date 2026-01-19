# Ellipse3D.getData Method

Parent Object: [Ellipse3D](Ellipse3D.md)  

## Description

Gets all of the data defining the ellipse.

## Syntax

"ellipse3D_var" is a variable referencing an [Ellipse3D](Ellipse3D.md) object.  

```python
(returnValue, center, normal, majorAxis, majorRadius, minorRadius) = ellipse3D_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The output center point of the ellipse. |
| normal | [Vector3D](Vector3D.md) | The output normal vector of the ellipse. |
| majorAxis | [Vector3D](Vector3D.md) | The output major axis of the ellipse |
| majorRadius | double | The output major radius of the of the ellipse. |
| minorRadius | double | The output minor radius of the of the ellipse. |

## Version

Introduced in version August 2014  

