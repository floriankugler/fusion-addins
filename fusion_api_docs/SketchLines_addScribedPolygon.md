# SketchLines.addScribedPolygon Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates either an inscribed or circumscribed n-sided polygon.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addScribedPolygon(centerPoint, edgeCount, angle, radius, isInscribed)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLineList](SketchLineList.md) | Returns a list of the sketch lines that were created to represent the polygon or null in the case of bad input. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Base](Base.md) | Either an existing SketchPoint or a Point3D object that defines the center point of the polygon. If a SketchPoint object is provided the point will continue to control the center of the polygon. |
| edgeCount | integer | The number of edges in the resulting polygon. |
| angle | double | Controls the rotation of the polygon around the center point. For a circumscribed polygon, this defines where the center of one of the edges will be positioned. For an inscribed polygon, this defines where one of the corners of the polygon will be positioned. |
| radius | double | The radius of the circle in centimeters that the polygon goes to, either outside (circumscribed) or inside (inscribed) the circle. |
| isInscribed | boolean | Specifies if a circumscribed or inscribed polygon should be created. |

## Version

Introduced in version January 2024  

