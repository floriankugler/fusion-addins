# Point3D.create Method

Parent Object: [Point3D](Point3D.md)  

## Description

Creates a transient 3D point object.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.Point3D.create()

# Uses optional arguments.
returnValue = adsk.core.Point3D.create(x, y, z)
```

## Return Value

| Type | Description |
|----|----|
| [Point3D](Point3D.md) | Returns the new Point3D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| x | double | The x coordinate of the point This is an optional argument whose default value is 0.0. |
| y | double | The y coordinate of the point This is an optional argument whose default value is 0.0. |
| z | double | The z coordinate of the point This is an optional argument whose default value is 0.0. |

## Samples

| Name | Description |
|----|----|
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchArcs.addByCenterStartSweep](SketchArcs_addByCenterStartaSweep_Sample.md) | Demonstrates the SketchArcs.addByCenterStartSweep method. |
| [SketchArcs.addByThreePoints](SketchArcs_addByThreePoints_Sample.md) | Demonstrates the SketchArcs.addByThreePoints method. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |
| [SketchArcs.breakCurve](SketchArcs_breakCurve_Sample.md) | Demonstrates the SketchArc.breakCurve method. |
| [SketchArcs.extend](SketchArcs_extend_Sample.md) | Demonstrates the SketchArc.extend method. |
| [SketchArcs.trim](SketchArcs_trim_Sample.md) | Demonstrates the SketchArc.trim method. |
| [SketchCircles.addByCenterRadius](SketchCircles_addByCenterRadius_Sample.md) | Demonstrates the SketchCircles.addByCenterRadius method. |
| [SketchCircles.addByThreePoints](SketchCircles_addByThreePoints_Sample.md) | Demonstrates the SketchCircles.addByThreePoints method. |
| [SketchCircles.addByThreeTangents](SketchCircles_addByThreeTangents_Sample.md) | Demonstrates the SketchCircles.addByThreeTangets method. |
| [SketchCircles.addByTwoPoints](SketchCircles_addByTwoPoints_Sample.md) | Demonstrates the SketchCircles.addByTwoPoints method. |
| [SketchEllipses.add](SketchEllipses_add_Sample.md) | Demonstrates the SketchEllipses.add method. |
| [SketchFittedSplines.add](SketchFittedSplines_add_Sample.md) | Demonstrates the SketchFittedSplines.add method. |
| [SketchLines.addThreePointRectangle](SketchLines_addThreePointRectangle_Sample.md) | Demonstrates the SketchLines.addThreePointRectangle method. |
| [SketchLines.addTwoPointRectangle](SketchLines_addTwoPointRectangle_Sample.md) | Demonstrates the SketchLines.addTwoPointRectangle method. |

## Version

Introduced in version August 2014  

