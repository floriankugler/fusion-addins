# SketchEllipses.add

## Description

Demonstrates the SketchEllipses.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Ellipses_add(sketch: adsk.fusion.Sketch): 
    # Define three points
    centerPoint = adsk.core.Point3D.create(0,0,0)
    majorAxisPoint = adsk.core.Point3D.create(10,0,0)
    throughPoint = adsk.core.Point3D.create(5,4,0)

    # Create an ellipse based on the points
    sketchEllipse = sketch.sketchCurves.sketchEllipses
    ellipse = sketchEllipse.add(centerPoint, majorAxisPoint, throughPoint)
```

