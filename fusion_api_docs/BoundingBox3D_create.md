# BoundingBox3D.create Method

Parent Object: [BoundingBox3D](BoundingBox3D.md)  

## Description

Creates a transient bounding box object. This object is created statically using the BoundingBox3D.create method.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.BoundingBox3D.create(minPoint, maxPoint)
```

## Return Value

| Type | Description |
|----|----|
| [BoundingBox3D](BoundingBox3D.md) | Returns the newly created bounding box or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| minPoint | [Point3D](Point3D.md) | The point that defines the minimum corner of the bounding box. |
| maxPoint | [Point3D](Point3D.md) | The point that defines the maximum corner of the bounding box. |

## Version

Introduced in version August 2014  

