# Circle3D.getData Method

Parent Object: [Circle3D](Circle3D.md)  

## Description

Gets all of the data defining the circle.

## Syntax

"circle3D_var" is a variable referencing a [Circle3D](Circle3D.md) object.  

```python
(returnValue, center, normal, radius) = circle3D_var.getData()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name   | Type                     | Description                            |
|--------|--------------------------|----------------------------------------|
| center | [Point3D](Point3D.md)   | The output center point of the circle. |
| normal | [Vector3D](Vector3D.md) | The output normal vector.              |
| radius | double                   | The output radius of the circle.       |

## Samples

| Name | Description |
|----|----|
| [Get Circle and Arc Data from Edge API Sample](GetCircleAndArcDataFromEdge_Sample.md) | Display the arc and circle geometric information from a selected circular edge. |

## Version

Introduced in version August 2014  

