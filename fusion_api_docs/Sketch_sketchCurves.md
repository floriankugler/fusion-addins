# Sketch.sketchCurves Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns the sketch curves collection associated with this sketch. This provides access to the existing sketch curves which is all geometry in the sketch except for sketch points. It is through this collection that new sketch geometry gets created.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.sketchCurves
```

## Property Value

This is a read only property whose value is a [SketchCurves](SketchCurves.md).

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [GeometricConstraint.addMidPont](GeometricConstraint_addMidPont_Sample.md) | Demonstrate the GeometricConstraint.addMidPont method. |
| [GeometricConstraints.addCoincident](GeometricConstraints_addCoincident_Sample.md) | Demonstrates the GeometricConstraints.addCoincident method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchArcs.addByCenterStartSweep](SketchArcs_addByCenterStartaSweep_Sample.md) | Demonstrates the SketchArcs.addByCenterStartSweep method. |
| [SketchArcs.addByThreePoints](SketchArcs_addByThreePoints_Sample.md) | Demonstrates the SketchArcs.addByThreePoints method. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |
| [SketchArcs.extend](SketchArcs_extend_Sample.md) | Demonstrates the SketchArc.extend method. |
| [SketchArcs.split](SketchArcs_split_Sample.md) | Demonstrates the SketchArc.split method. |
| [SketchArcs.trim](SketchArcs_trim_Sample.md) | Demonstrates the SketchArc.trim method. |
| [SketchCircles.addByThreePoints](SketchCircles_addByThreePoints_Sample.md) | Demonstrates the SketchCircles.addByThreePoints method. |
| [SketchCircles.addByThreeTangents](SketchCircles_addByThreeTangents_Sample.md) | Demonstrates the SketchCircles.addByThreeTangets method. |
| [SketchCircles.addByTwoPoints](SketchCircles_addByTwoPoints_Sample.md) | Demonstrates the SketchCircles.addByTwoPoints method. |
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |
| [SketchDimensions.addDiameterDimension](SketchDimension_addDiameterDimension_Sample.md) | Demonstrates the SketchDimension.addDiameterDimension method. |
| [SketchEllipses.add](SketchEllipses_add_Sample.md) | Demonstrates the SketchEllipses.add method. |
| [SketchFittedSplines.add](SketchFittedSplines_add_Sample.md) | Demonstrates the SketchFittedSplines.add method. |
| [SketchFixedSplines.addByNurbsCurve](SketchFixedSplines_addByNurbsCurve_Sample.md) | Demonstrates the SketchFixedSplines.addByNurbsCurve method. |
| [SketchLines.addDistanceChamfer](SketchLines_addDistanceChamfer_Sample.md) | Demonstrates the SketchLines.addDistanceChamfer method. |
| [SketchLines.addThreePointRectangle](SketchLines_addThreePointRectangle_Sample.md) | Demonstrates the SketchLines.addThreePointRectangle method. |
| [SketchLines.addTwoPointRectangle](SketchLines_addTwoPointRectangle_Sample.md) | Demonstrates the SketchLines.addTwoPointRectangle method. |

## Version

Introduced in version August 2014  

