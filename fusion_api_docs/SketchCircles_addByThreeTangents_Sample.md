# SketchCircles.addByThreeTangents

## Description

Demonstrates the SketchCircles.addByThreeTangets method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Circles_addByThreeTangents(sketch: adsk.fusion.Sketch):
    # Create three lines and a point
    lines = sketch.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(3, 1, 0))
    line2 = lines.addByTwoPoints(adsk.core.Point3D.create(4, 3, 0), adsk.core.Point3D.create(2, 4, 0))
    line3 = lines.addByTwoPoints(adsk.core.Point3D.create(-1, 0, 0), adsk.core.Point3D.create(0, 4, 0))
    hintPoint = adsk.core.Point3D.create(0, 0, 0)

    # Create a circle based on the lines
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByThreeTangents(line1, line2, line3, hintPoint)
```

