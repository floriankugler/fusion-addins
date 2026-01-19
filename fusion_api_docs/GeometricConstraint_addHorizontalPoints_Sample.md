# GeometricConstraint.addHorizontalPoints

## Description

Demonstrates the GeometricConstraint.addHorizontalPoints method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addHorizontalPoints(sketch: adsk.fusion.Sketch):
    # Create two sketch points.
    pointOne = sketch.sketchPoints.add(adsk.core.Point3D.create(0, 0, 0))
    pointTwo = sketch.sketchPoints.add(adsk.core.Point3D.create(6, 9, 0))
    
    # Create a Horizontal constraint between the two points.
    constraints = sketch.geometricConstraints
    horizontalPointConstraint = constraints.addHorizontalPoints(pointOne, pointTwo)
```

