# SketchPoint.add

## Description

Demonstrates the SketchPoint.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def  demo_SketchPoint_add(sketch: adsk.fusion.Sketch):
    somePoint = adsk.core.Point3D.create(5, 4, 0)
    sketchPoints = sketch.sketchPoints
    point = sketchPoints.add(somePoint)
```

