# SketchCircles.addByCenterRadius

## Description

Demonstrates the SketchCircles.addByCenterRadius method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Circles_addByCenterRadius(sketch: adsk.fusion.Sketch):
    # Define a center point and radius
    centerPoint = adsk.core.Point3D.create(0, 0, 0)
    radius = 2

    # Create a circle using the center point and radius 
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(centerPoint, radius)
```

