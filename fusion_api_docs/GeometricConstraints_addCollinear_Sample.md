# GeometricConstraints.addCollinear

## Description

Demonstrates the GeometricConstraints.addCollinear method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addCollinear(sketch: adsk.fusion.Sketch):
    # Create two sketch lines.
    lineOne = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                             adsk.core.Point3D.create(5, 0, 0))
    lineTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 10, 0),
                                                             adsk.core.Point3D.create(10, 15, 0))

    # Create a collinear constraint between the lines
    constraints = sketch.geometricConstraints
    collinearConstraint = constraints.addCollinear(lineOne, lineTwo)
```

