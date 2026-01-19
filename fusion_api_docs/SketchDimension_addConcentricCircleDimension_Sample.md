# SketchDimensions.addConcentricCicleDimension

## Description

Demonstrates the SketchDimension.addConcentricCircleDimension method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Dimension_addConcentricCircleDimension(sketch: adsk.fusion.Sketch):
    pointOne = adsk.core.Point3D.create(0,0,0)
    pointTwo = adsk.core.Point3D.create(10,10,0)
    pointThree = adsk.core.Point3D.create(-5,-5,0)
    pointFour = adsk.core.Point3D.create(-10,-10,0)
    
    # Create the circles and text point for parameters
    circleOne = sketch.sketchCurves.sketchCircles.addByTwoPoints(pointOne, pointTwo)
    circleTwo = sketch.sketchCurves.sketchCircles.addByTwoPoints(pointThree, pointFour) 
    textPoint = adsk.core.Point3D.create(-2,-2,0)

    # Create the concentric circle
    dim = sketch.sketchDimensions
    concentricCircleDimension = dim.addConcentricCircleDimension(circleOne, circleTwo, textPoint)
```

