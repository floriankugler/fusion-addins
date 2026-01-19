# OrientedBoundingBox3D.create Method

Parent Object: [OrientedBoundingBox3D](OrientedBoundingBox3D.md)  

## Description

Creates a transient oriented bounding box object.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.OrientedBoundingBox3D.create(centerPoint, lengthDirection, widthDirection, length, width, height)
```

## Return Value

| Type | Description |
|----|----|
| [OrientedBoundingBox3D](OrientedBoundingBox3D.md) | Returns the new oriented bounding box. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Point3D](Point3D.md) | The center point of the oriented box. |
| lengthDirection | [Vector3D](Vector3D.md) | A Vector3D object that defines the direction of the length of the oriented bounding box. The magnitude of the vector is ignored and just the direction is used. |
| widthDirection | [Vector3D](Vector3D.md) | A Vector3D object that defines the direction of the width of the oriented bounding box. The magnitude of the vector is ignored and just the direction is used. The width direction must be perpendicular to the length direction. |
| length | double | The length of the oriented bounding box in centimeters. |
| width | double | The width of the oriented bounding box in centimeters. The width of the box is always perpendicular to the length. |
| height | double | The height of the oriented bounding box in centimeters. The height of the box is perpendicular to the length-width plane using the right-hand rule where you cross the length into the width. |

## Version

Introduced in version December 2017  

