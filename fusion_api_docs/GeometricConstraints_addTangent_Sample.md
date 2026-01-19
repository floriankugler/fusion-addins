# GeometricConstraints.addTangent

## Description

Demonstrates the GeometricConstraints.addTangent method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addTangent(sketch: adsk.fusion.Sketch):
   # Create a sketch line and sketch arc that is connected to the line.
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(adsk.core.Point3D.create(0, 0, 0), 
                                                          adsk.core.Point3D.create(10, 5, 0),
                                                          adsk.core.Point3D.create(0, 10, 0))
    line = sketch.sketchCurves.sketchLines.addByTwoPoints(arc.endSketchPoint, adsk.core.Point3D.create(-5, 12, 0))

    # Create a tangent constraint between the line and arc.
    constraints = sketch.geometricConstraints
    tangentConstraint = constraints.addTangent(arc, line)
```

