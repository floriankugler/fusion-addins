# SketchDimensions.addAngularDimension

## Description

Demonstrates the SketchDimension.addAngularDimension method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Dimension_addAngularDimension(sketch: adsk.fusion.Sketch):
    # Create points for the lines
    startPoint = adsk.core.Point3D.create(6, 0, 0)
    endPoint = adsk.core.Point3D.create(0, 0, 0)

    # Create the lines and text point for parameters
    lines = sketch.sketchCurves.sketchLines
    lineOne = lines.addByTwoPoints(startPoint, endPoint)
    lineTwo = lines.addByTwoPoints(lineOne.endSketchPoint, adsk.core.Point3D.create(5, 4, 0))
    textPoint = adsk.core.Point3D.create(7, 2, 0)

    # Create the angular dimension
    dimensions = sketch.sketchDimensions
    angularDimension = dimensions.addAngularDimension(lineOne, lineTwo, textPoint)
```

