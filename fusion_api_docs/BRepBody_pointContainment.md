# BRepBody.pointContainment Method

Parent Object: [BRepBody](BRepBody.md)  

## Description

Determines the relationship of the input point with respect to this body.

## Syntax

"bRepBody_var" is a variable referencing a [BRepBody](BRepBody.md) object.

```python
returnValue = bRepBody_var.pointContainment(point)
```

## Return Value

| Type | Description |
|----|----|
| [PointContainment](PointContainment.md) | Returns a value from the PointContainment enum indicating the relationship of the input point to the body. |

## Parameters

| Name  | Type                   | Description                                |
|-------|------------------------|--------------------------------------------|
| point | [Point3D](Point3D.md) | The point to do the containment check for. |

## Version

Introduced in version August 2014  

