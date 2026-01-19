# OrientedBoundingBox3D.contains Method

Parent Object: [OrientedBoundingBox3D](OrientedBoundingBox3D.md)  

## Description

Determines if the specified point lies within the oriented bounding box.

## Syntax

"orientedBoundingBox3D_var" is a variable referencing an [OrientedBoundingBox3D](OrientedBoundingBox3D.md) object.

```python
returnValue = orientedBoundingBox3D_var.contains(point)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the point lies within the bounding box. |

## Parameters

| Name  | Type                   | Description                         |
|-------|------------------------|-------------------------------------|
| point | [Point3D](Point3D.md) | The point to test containment with. |

## Samples

| Name                                       | Description               |
|--------------------------------------------|---------------------------|
| [Measure Sample](MeasureSample_Sample.md) | Measure related functions |

## Version

Introduced in version December 2017  

