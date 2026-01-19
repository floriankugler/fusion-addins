# SketchEllipticalArcs.addByEndPoints Method

Parent Object: [SketchEllipticalArcs](SketchEllipticalArcs.md)  

## Description

Creates an elliptical sketch arc where the sweep of the arc is defined by two points.

## Syntax

"sketchEllipticalArcs_var" is a variable referencing a [SketchEllipticalArcs](SketchEllipticalArcs.md) object.

```python
returnValue = sketchEllipticalArcs_var.addByEndPoints(centerPoint, majorAxis, minorAxis, startPoint, endPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEllipticalArc](SketchEllipticalArc.md) | Returns the newly created SketchEllipticalArc or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Base](Base.md) | The center point of the ellipse. This can be either an existing SketchPoint or a Point3D object. |
| majorAxis | [Vector3D](Vector3D.md) | The direction of the major axis. The magnitude of this vector defines the major radius. |
| minorAxis | [Vector3D](Vector3D.md) | The direction of the minor axis. The magnitude of this vector defines the minor radius. This vector should be perpendicular to the major axis. |
| startPoint | [Base](Base.md) | The start point of the elliptical arc. This can be either an existing SketchPoint or a Point3D object. The point should lie on the defined ellipse. |
| endPoint | [Base](Base.md) | The end point of the elliptical arc. This can be either an existing SketchPoint or a Point3D object. The point should lie on the defined ellipse and the elliptical arc is defined by a counterclockwise sweep from the start point to the end point. |

## Version

Introduced in version May 2022  

