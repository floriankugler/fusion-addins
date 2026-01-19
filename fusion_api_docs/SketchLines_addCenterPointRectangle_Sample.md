# SketchLines.addCenterPointRectangle

## Description

Demonstrates the SketchLines.addCenterPointRectangle method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addCenterPointRectangle(sketch: adsk.fusion.Sketch):
    # Define two points
    centerPoint = adsk.core.Point3D.create(5, 5, 0)
    cornerPoint = adsk.core.Point3D.create(25, 25, 0)

    # Create the rectangle using the points
    rectangles = sketch.sketchCurves.sketchLines 
    rectangle = rectangles.addCenterPointRectangle(centerPoint, cornerPoint)
```

