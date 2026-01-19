# BoundingBox3D.expand Method

Parent Object: [BoundingBox3D](BoundingBox3D.md)  

## Description

Expands the size of bounding box to include the specified point.

## Syntax

"boundingBox3D_var" is a variable referencing a [BoundingBox3D](BoundingBox3D.md) object.

```python
returnValue = boundingBox3D_var.expand(point)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the expansion was successful. |

## Parameters

| Name  | Type                   | Description                                   |
|-------|------------------------|-----------------------------------------------|
| point | [Point3D](Point3D.md) | The point to include within the bounding box. |

## Version

Introduced in version August 2014  

