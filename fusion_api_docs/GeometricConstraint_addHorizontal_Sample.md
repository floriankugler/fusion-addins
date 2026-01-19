# GeometricConstraint.addHorizontal

## Description

Demonstrates the GeometricConstraint.addHorizontal method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addHorizontal(sketch: adsk.fusion.Sketch):
    # Create a sketch line.
    line = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                            adsk.core.Point3D.create(0, 10, 0))

    # Add a horizontal constraint to the sketch line.
    constraints = sketch.geometricConstraints
    horizontalConstraint = constraints.addHorizontal(line)
```

