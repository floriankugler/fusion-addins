# GeometricConstraints.addEqual

## Description

Demonstrates the GeometricConstraints.addEqual method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addEqual(sketch: adsk.fusion.Sketch):
    # Create two sketch lines.. 
    curveOne = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                                adsk.core.Point3D.create(10, 0, 0))
    curveTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 10, 0),
                                                                adsk.core.Point3D.create(10, 10, 0))
    
    # Create an equal constraint between the two lines to make them equal length.
    constraints = sketch.geometricConstraints
    equalConstraint = constraints.addEqual(curveOne, curveTwo)
```

