# Arc3D.setAxes Method

Parent Object: [Arc3D](Arc3D.md)  

## Description

Sets the normal and reference vectors of the arc.

## Syntax

"arc3D_var" is a variable referencing an [Arc3D](Arc3D.md) object.

```python
returnValue = arc3D_var.setAxes(normal, referenceVector)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| normal | [Vector3D](Vector3D.md) | The new normal vector. |
| referenceVector | [Vector3D](Vector3D.md) | The new reference vector from which the start and end angles are measured from. The reference vector must be perpendicular to the normal vector. |

## Version

Introduced in version August 2014  

