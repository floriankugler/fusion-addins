# BRepLump.pointContainment Method

Parent Object: [BRepLump](BRepLump.md)  

## Description

Determines the relationship of the input point with respect to this lump.

## Syntax

"bRepLump_var" is a variable referencing a [BRepLump](BRepLump.md) object.

```python
returnValue = bRepLump_var.pointContainment(point)
```

## Return Value

| Type | Description |
|----|----|
| [PointContainment](PointContainment.md) | Returns a value from the PointContainment enum indicating the relationship of the input point to the lump. |

## Parameters

| Name  | Type                   | Description                                |
|-------|------------------------|--------------------------------------------|
| point | [Point3D](Point3D.md) | The point to do the containment check for. |

## Version

Introduced in version August 2014  

