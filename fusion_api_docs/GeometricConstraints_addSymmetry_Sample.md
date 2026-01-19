# GeometricConstraints.addSymmetry

## Description

Demonstrates the GeometricConstraints.addSymmetry method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addSymmetry(sketch: adsk.fusion.Sketch):
    # Create two sketch circles.
    leftCircle = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(2, 3, 0), 3)
    rightCircle = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(10, 5, 0), 2)
    
    # Create a sketch line.
    symmetryLine = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(6, 0, 0),
                                                                  adsk.core.Point3D.create(6, 7, 0))    
    
    # Add a symmetric constraint to make the circles symmetric around the line.
    constraints = sketch.geometricConstraints
    symmetryConstraint = constraints.addSymmetry(leftCircle, rightCircle, symmetryLine)
```

