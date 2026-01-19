# SketchArcs.trim

## Description

Demonstrates the SketchArc.trim method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_trim(sketch: adsk.fusion.Sketch):
    # Define three points and create an arc along those points
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    alongPoint = adsk.core.Point3D.create(5, 0, 0)
    endPoint = adsk.core.Point3D.create(8, 7, 0)
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

    # Creat a line that crosses the arc that will be used to trim to.
    lines = sketch.sketchCurves.sketchLines
    lineStart = adsk.core.Point3D.create(4, -2, 0)
    lineEnd = adsk.core.Point3D.create(5, 3, 0)
    line = lines.addByTwoPoints(lineStart, lineEnd)

    # trim the arc keeping the side where start point is.
    trimmedArc = arc.trim(arc.startSketchPoint.geometry)
```

