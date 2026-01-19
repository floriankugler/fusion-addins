# SketchArcs.breakCurve

## Description

Demonstrates the SketchArc.breakCurve method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_breakCurve(sketch: adsk.fusion.Sketch):
    # Define three points and create an arc along those points
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    alongPoint = adsk.core.Point3D.create(5, 0, 0)
    endPoint = adsk.core.Point3D.create(8, 7, 0)
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

    # Draw two lines that cross the arc.
    lines = sketch.sketchCurves.sketchLines
    lineStart = adsk.core.Point3D.create(3, 4, 0)
    lineEnd = adsk.core.Point3D.create(4, -2, 0)
    line1 = lines.addByTwoPoints(lineStart, lineEnd)
    lineStart = adsk.core.Point3D.create(6, 5, 0)
    lineEnd = adsk.core.Point3D.create(7, -1, 0)
    line2 = lines.addByTwoPoints(lineStart, lineEnd)

    # break the arc 
    segmentPoint = adsk.core.Point3D.create(5, 1, 0)
    breakCurve = arc.breakCurve(segmentPoint)
```

