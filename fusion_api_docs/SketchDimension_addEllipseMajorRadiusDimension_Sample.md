# SketchDimensions.AddEllipseMajorRadiusDimension

## Description

Demonstrates the SketchDimension.addEllipseMajorRadiusDimension method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Dimension_addEllipseMajorRadiusDimension(sketch: adsk.fusion.Sketch):
    centerPoint = adsk.core.Point3D.create(0, 0, 0)
    majorAxisPoint = adsk.core.Point3D.create(10, 0, 0)
    throughPoint = adsk.core.Point3D.create(5, 4, 0)

    # Create ellipse and text point for parameters
    ellipse = sketch.sketchCurves.sketchEllipses.add(centerPoint, majorAxisPoint, throughPoint) 
    textPoint = adsk.core.Point3D.create(7.5, 7, 0)

    # Create the ellipse 
    dim = sketch.sketchDimensions
    majorRadiusDimension = dim.addEllipseMajorRadiusDimension(ellipse, textPoint)
```

