# SketchArcs.split

## Description

Demonstrates the SketchArc.split method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Arcs_split(sketch: adsk.fusion.Sketch):
    # Define three points and create an arc along those points
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    alongPoint = adsk.core.Point3D.create(5, 0, 0)
    endPoint = adsk.core.Point3D.create(8, 7, 0)
    arcs = sketch.sketchCurves.sketchArcs
    arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

    # Get the midpoint of the arc.
    curveEval = arc.geometry.evaluator
    (_, startParam, endParam) = curveEval.getParameterExtents()
    (_, midPoint) = curveEval.getPointAtParameter((startParam + endParam) / 2)

    # Split the arc
    splitArc = arc.split(midPoint)
```

