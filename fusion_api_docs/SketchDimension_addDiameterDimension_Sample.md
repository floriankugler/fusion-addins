# SketchDimensions.addDiameterDimension

## Description

Demonstrates the SketchDimension.addDiameterDimension method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Dimension_addDiameterDimension(sketch: adsk.fusion.Sketch):
    pointOne = adsk.core.Point3D.create(0, 0, 0)
    pointTwo = adsk.core.Point3D.create(10, 10, 0)

    # Create the entity and text point for parameters
    entity = sketch.sketchCurves.sketchCircles.addByTwoPoints(pointOne, pointTwo)
    textPoint = adsk.core.Point3D.create(12, 12, 0)

    # Create the circle using diameter between the two points
    dimensions = sketch.sketchDimensions
    circleDimension = dimensions.addDiameterDimension(entity, textPoint)
```

