# SketchArcs.addFillet

## Description

Demonstrates the SketchArcs.addFillet method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_addFillet(sketch: adsk.fusion.Sketch):
    # Create two connected lines
    lines = sketch.sketchCurves.sketchLines
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    endPoint = adsk.core.Point3D.create(3, 1, 0)
    line1 = lines.addByTwoPoints(startPoint, endPoint)
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(1, 4, 0))

    # Create arc by adding fillet between the two lines
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, 1)
```

