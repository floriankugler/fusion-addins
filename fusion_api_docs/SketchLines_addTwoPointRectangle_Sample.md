# SketchLines.addTwoPointRectangle

## Description

Demonstrates the SketchLines.addTwoPointRectangle method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addTwoPointRectangle(sketch: adsk.fusion.Sketch):
    # Define two points
    pointOne = adsk.core.Point3D.create(0, 0, 0)
    pointTwo = adsk.core.Point3D.create(5, 15, 0)

    # Create the rectangle using the points
    rectangles = sketch.sketchCurves.sketchLines 
    rectangle = rectangles.addTwoPointRectangle(pointOne, pointTwo)
```

