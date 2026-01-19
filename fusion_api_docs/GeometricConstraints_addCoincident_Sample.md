# GeometricConstraints.addCoincident

## Description

Demonstrates the GeometricConstraints.addCoincident method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addCoincident(sketch: adsk.fusion.Sketch):
    # Create a sketch point and arc. 
    point = sketch.sketchPoints.add(adsk.core.Point3D.create(0, 0, 0))
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(adsk.core.Point3D.create(15, 14, 0),
                                                            adsk.core.Point3D.create(9, 11, 0),
                                                            adsk.core.Point3D.create(7, 13, 0))

    # Create a coincident constraint between the point and the arc.
    constraints = sketch.geometricConstraints
    coincidentConstraint = constraints.addCoincident(point, arc)
```

