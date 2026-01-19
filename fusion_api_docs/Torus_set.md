# Torus.set Method

Parent Object: [Torus](Torus.md)  

## Description

Sets all of the data defining the torus.

## Syntax

"torus_var" is a variable referencing a [Torus](Torus.md) object.

```python
returnValue = torus_var.set(origin, axis, majorRadius, minorRadius)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| origin | [Point3D](Point3D.md) | The origin point (center) of the torus. |
| axis | [Vector3D](Vector3D.md) | The center axis of the torus. |
| majorRadius | double | The major radius of the torus. |
| minorRadius | double | The minor radius of the torus. |

## Version

Introduced in version August 2014  

