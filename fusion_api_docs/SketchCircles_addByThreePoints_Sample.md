# SketchCircles.addByThreePoints

## Description

Demonstrates the SketchCircles.addByThreePoints method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Circles_addByThreePoints(sketch: adsk.fusion.Sketch):
    # Define three points 
    pointOne = adsk.core.Point3D.create(0, 0, 0)
    pointTwo = adsk.core.Point3D.create(5, 5, 0)
    pointThree = adsk.core.Point3D.create(9, 14, 0)

    # Create a circle based on the points 
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByThreePoints(pointOne, pointTwo, pointThree)
```

