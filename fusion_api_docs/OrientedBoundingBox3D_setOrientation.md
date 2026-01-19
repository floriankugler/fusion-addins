# OrientedBoundingBox3D.setOrientation Method

Parent Object: [OrientedBoundingBox3D](OrientedBoundingBox3D.md)  

## Description

Sets the orientation of the oriented bounding box.

## Syntax

"orientedBoundingBox3D_var" is a variable referencing an [OrientedBoundingBox3D](OrientedBoundingBox3D.md) object.

```python
returnValue = orientedBoundingBox3D_var.setOrientation(lengthDirection, widthDirection)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| lengthDirection | [Vector3D](Vector3D.md) | A Vector3D object that defines the direction of the length of the oriented bounding box. The magnitude of the vector is ignored and just the direction is used. |
| widthDirection | [Vector3D](Vector3D.md) | A Vector3D object that defines the direction of the width of the oriented bounding box. The magnitude of the vector is ignored and just the direction is used. The width direction must be perpendicular to the length direction. |

## Version

Introduced in version December 2017  

