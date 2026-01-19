# SketchCircles.addByTwoTangents

## Description

Demonstrates the SketchCircles.addByTwoTangets method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Circles_addByTwoTangents(sketch: adsk.fusion.Sketch):
    # Create three lines.
    lines = sketch.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(-10, 0, 0), adsk.core.Point3D.create(10, 0, 0))
    line2 = lines.addByTwoPoints(adsk.core.Point3D.create(0, -10, 0), adsk.core.Point3D.create(0, 10, 0))

    # Define a hint point to create the circle in the positive quadrant.
    hintPoint = adsk.core.Point3D.create(5, 5, 0)

    # Create a circle that is tangent to the two lines.
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByTwoTangents(line1, line2, 5, hintPoint)

    # If you want tangent constraints between the circle and the line, you need to create them.
    geomConstraints = sketch.geometricConstraints
    geomConstraints.addTangent(line1, circle)
    geomConstraints.addTangent(line2, circle)
```

