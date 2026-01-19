# SketchArcs.addByCenterStartSweep

## Description

Demonstrates the SketchArcs.addByCenterStartSweep method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_addByCenterStartSweep(sketch: adsk.fusion.Sketch):
    # Define two points and specify the sweep angle
    startPoint = adsk.core.Point3D.create(5, 5, 0)
    centerPoint = adsk.core.Point3D.create(15, 0, 0)
    sweepAngle = -135.0

    # Create an arc centered at the specified point
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addByCenterStartSweep(centerPoint, startPoint, sweepAngle)
```

