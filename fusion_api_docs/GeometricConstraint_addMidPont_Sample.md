# GeometricConstraint.addMidPont

## Description

Demonstrate the GeometricConstraint.addMidPont method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addMidPoint(sketch: adsk.fusion.Sketch):
    # Create a sketch point and arc. 
    point = sketch.sketchPoints.add(adsk.core.Point3D.create(15, 15, 0))
    arc = sketch.sketchCurves.sketchArcs.addByThreePoints(adsk.core.Point3D.create(0, 0, 0), 
                                                          adsk.core.Point3D.create(10, 5, 0),
                                                          adsk.core.Point3D.create(0, 10, 0))

    # Add a midpoint constraint between the point and arc
    constraints = sketch.geometricConstraints
    midPointConstraint = constraints.addMidPoint(point, arc)
```

