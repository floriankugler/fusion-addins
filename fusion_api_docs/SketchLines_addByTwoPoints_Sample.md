# SketchLines.addByTwoPoints

## Description

Demonstrates the SketchLines.addByTwoPoints method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addByTwoPoints(sketch: adsk.fusion.Sketch):
    # Define two points
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    endPoint = adsk.core.Point3D.create(10, 0, 0)
    
    # Create the line using the two points
    lines = sketch.sketchCurves.sketchLines
    line = lines.addByTwoPoints(startPoint, endPoint)
```

