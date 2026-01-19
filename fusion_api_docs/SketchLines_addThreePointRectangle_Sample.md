# SketchLines.addThreePointRectangle

## Description

Demonstrates the SketchLines.addThreePointRectangle method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addThreePointRectangle(sketch: adsk.fusion.Sketch):
    # Define three points
    pointOne = adsk.core.Point3D.create(0, 0, 0)
    pointTwo = adsk.core.Point3D.create(5, 15, 0)
    pointThree = adsk.core.Point3D.create(-5, -6, 0)

    # Create the rectangle using the points
    rectangles = sketch.sketchCurves.sketchLines 
    rectangle = rectangles.addThreePointRectangle(pointOne, pointTwo, pointThree)
```

