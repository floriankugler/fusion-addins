# SketchFixedSplines.addByNurbsCurve

## Description

Demonstrates the SketchFixedSplines.addByNurbsCurve method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_FixedSplines_addByNurbsCurve(sketch: adsk.fusion.Sketch):
    # Define three points and create an arc along those points
    pointOne = adsk.core.Point3D.create(0,0,0)
    pointTwo = adsk.core.Point3D.create(6,9,0)
    pointThree = adsk.core.Point3D.create(15,12,0)
    arc3D = adsk.core.Arc3D.createByThreePoints(pointOne, pointTwo, pointThree)
    nurbsCurve = arc3D.asNurbsCurve

    # Create the spline using the 3D curve 
    splines = sketch.sketchCurves.sketchFixedSplines
    fixedSpline = splines.addByNurbsCurve(nurbsCurve)
```

