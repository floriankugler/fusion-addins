# Torus.getData Method

Parent Object: [Torus](Torus.md)  

## Description

Gets all of the data defining the torus.

## Syntax

"torus_var" is a variable referencing a [Torus](Torus.md) object.  

```python
(returnValue, origin, axis, majorRadius, minorRadius) = torus_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The output origin point (center) of the torus. |
| axis | [Vector3D](Vector3D.md) | The output center axis of the torus. |
| majorRadius | double | The output major radius of the torus. |
| minorRadius | double | The output minor radius of the torus. |

## Version

Introduced in version August 2014  

