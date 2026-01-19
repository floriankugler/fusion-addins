# Arc3D.getData Method

Parent Object: [Arc3D](Arc3D.md)  

## Description

Gets all of the data defining the arc.

## Syntax

"arc3D_var" is a variable referencing an [Arc3D](Arc3D.md) object.  

```python
(returnValue, center, normal, referenceVector, radius, startAngle, endAngle) = arc3D_var.getData()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point3D](Point3D.md) | The output center point of the arc. |
| normal | [Vector3D](Vector3D.md) | The output normal vector. |
| referenceVector | [Vector3D](Vector3D.md) | The output reference vector. |
| radius | double | The output radius of the arc. |
| startAngle | double | The output start angle in radians. This angle is measured from the reference vector using the right hand rule around the normal vector. |
| endAngle | double | The output end angle in radians. This angle is measured from the reference vector using the right hand rule around the normal vector. |

## Samples

| Name | Description |
|----|----|
| [Get Circle and Arc Data from Edge API Sample](GetCircleAndArcDataFromEdge_Sample.md) | Display the arc and circle geometric information from a selected circular edge. |

## Version

Introduced in version August 2014  

