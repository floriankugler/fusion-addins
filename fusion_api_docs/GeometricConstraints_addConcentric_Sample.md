# GeometricConstraints.addConcentric

## Description

Demonstrates the GeometricConstraints.addConcentric method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addConcentric(sketch: adsk.fusion.Sketch):
    # Create two sketch circles. 
    entityOne = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(2, 3, 0),
                                                                    radius = 3)
    entityTwo = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(6, 12, 0),
                                                                    radius = 2)
    
    # Create a concentric constraint beween the circles.
    constraints = sketch.geometricConstraints
    concentricConstraint = constraints.addConcentric(entityOne, entityTwo)
```

