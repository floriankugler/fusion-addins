# SketchDimensions.addOffsetDimension

## Description

Demonstrates the SketchDimension.addOffsetDimension method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Dimension_addOffsetDimension(sketch: adsk.fusion.Sketch):
    # Create the line and second entity for parameters
    line = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                          adsk.core.Point3D.create(10, 0, 0)  )
    entityTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 10, 0),
                                                                adsk.core.Point3D.create(10, 10, 0))

    textPoint = adsk.core.Point3D.create(13, 5, 0)

    # Create the lines
    dim = sketch.sketchDimensions
    offsetDimension = dim.addOffsetDimension(line, entityTwo, textPoint)
```

