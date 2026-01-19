# BRepShell.pointContainment Method

Parent Object: [BRepShell](BRepShell.md)  

## Description

Determines the relationship of the input point with respect to this shell.

## Syntax

"bRepShell_var" is a variable referencing a [BRepShell](BRepShell.md) object.

```python
returnValue = bRepShell_var.pointContainment(point)
```

## Return Value

| Type | Description |
|----|----|
| [PointContainment](PointContainment.md) | Returns a value from the PointContainment enum indicating the relationship of the input point to the shell. |

## Parameters

| Name  | Type                   | Description                                |
|-------|------------------------|--------------------------------------------|
| point | [Point3D](Point3D.md) | The point to do the containment check for. |

## Version

Introduced in version August 2014  

