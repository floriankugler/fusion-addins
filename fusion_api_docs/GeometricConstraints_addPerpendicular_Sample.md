# GeometricConstraints.addPerpendicular

## Description

Demonstrates the GeometricConstraints.addPerpendicular method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addPerpendicular(sketch: adsk.fusion.Sketch):
    # Create two sketch lines.
    lineOne = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                             adsk.core.Point3D.create(0, 10, 0))
    lineTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(2, 5, 0),
                                                             adsk.core.Point3D.create(13, 10, 0))

    # Create a perpendicular constraint between the two lines. 
    constraints = sketch.geometricConstraints
    parallelConstraint = constraints.addPerpendicular(lineOne, lineTwo)
```

