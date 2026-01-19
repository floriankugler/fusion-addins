# SketchFittedSplines.add

## Description

Demonstrates the SketchFittedSplines.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_FittedSplines_add(sketch: adsk.fusion.Sketch):
    # Create an object collection for the points.
    points = adsk.core.ObjectCollection.create()

    # Define the points the spline with fit through.
    points.add(adsk.core.Point3D.create(0, 0, 0))
    points.add(adsk.core.Point3D.create(5, 1, 0))
    points.add(adsk.core.Point3D.create(6, 4, 3))
    points.add(adsk.core.Point3D.create(7, 6, 6))
    points.add(adsk.core.Point3D.create(2, 3, 0))
    points.add(adsk.core.Point3D.create(0, 1, 0))

    # Create the spline 
    splines = sketch.sketchCurves.sketchFittedSplines 
    spline = splines.add(points)
```

