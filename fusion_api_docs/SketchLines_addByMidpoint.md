# SketchLines.addByMidpoint Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates a sketch line where the first point is the midpoint and the second point is one endpoint. The system automatically calculates the other endpoint to create a line where the first point is exactly at the midpoint.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addByMidpoint(midPoint, secondPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLine](SketchLine.md) | Returns the newly created SketchLine object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| midPoint | [Base](Base.md) | The midpoint of the line. It can be a SketchPoint or Point3D object. |
| secondPoint | [Base](Base.md) | One endpoint of the line. It can be a SketchPoint or Point3D object. The other endpoint will be calculated automatically. |

## Version

Introduced in version January 2026  

