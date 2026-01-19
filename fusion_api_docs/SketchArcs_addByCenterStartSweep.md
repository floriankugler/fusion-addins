# SketchArcs.addByCenterStartSweep Method

Parent Object: [SketchArcs](SketchArcs.md)  

## Description

Creates a sketch arc that is always parallel to the x-y plane of the sketch and is centered at the specified point.

## Remarks

Sketch arcs always exist in a counterclockwise direction. Even though you can specify a negative sweep to define an arc in a clockwise direction, the result will still be a counterclockwise arc. This means if you query the created sketch arc, the start and end points may be opposite of what you expect.

## Syntax

"sketchArcs_var" is a variable referencing a [SketchArcs](SketchArcs.md) object.

```python
returnValue = sketchArcs_var.addByCenterStartSweep(centerPoint, startPoint, sweepAngle)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the newly created SketchArc object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Base](Base.md) | The center point of the arc. This can be either an existing SketchPoint or a Point3D object. |
| startPoint | [Base](Base.md) | The start point of the arc. The distance between this point and the center defines the radius of the arc. This can be either an existing SketchPoint or a Point3D object. |
| sweepAngle | double | The sweep of the arc. This is defined in radians and a positive value defines a counter-clockwise sweep. |

## Samples

| Name | Description |
|----|----|
| [SketchArcs.addByCenterStartSweep](SketchArcs_addByCenterStartaSweep_Sample.md) | Demonstrates the SketchArcs.addByCenterStartSweep method. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |

## Version

Introduced in version August 2014  

