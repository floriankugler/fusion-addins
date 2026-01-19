# SketchArcs.extend

## Description

Demonstrates the SketchArc.extend method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_extend(sketch: adsk.fusion.Sketch):
    # Define three points and create an arc along those points
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    alongPoint = adsk.core.Point3D.create(5, 3, 0)
    endPoint = adsk.core.Point3D.create(8, 0, 0)
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

    # Create a line to extend the arc to.
    lineStart = adsk.core.Point3D.create(-2, -3, 0)
    lineEnd = adsk.core.Point3D.create(10, -3, 0)
    lines = sketch.sketchCurves.sketchLines
    line = lines.addByTwoPoints(lineStart, lineEnd)

    # Extend the end point of the arc. 
    extendedCurve = arc.extend(endPoint)
```

