# SketchCircles.addByTwoPoints

## Description

Demonstrates the SketchCircles.addByTwoPoints method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Circles_addByTwoPoints(sketch: adsk.fusion.Sketch):
    # Define two points
    pointOne = adsk.core.Point3D.create(1, 1, 0)
    pointTwo = adsk.core.Point3D.create(8, 8, 0)

    # Create a circle based on the two points
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByTwoPoints(pointOne, pointTwo)
```

