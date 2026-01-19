# SketchLines.addAngleChamfer

## Description

Demonstrates the SketchLines.addAngleChamfer method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addAngleChamfer(sketch: adsk.fusion.Sketch): 
    # Create lines for the angle chamfer parameters
    lineOne = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                             adsk.core.Point3D.create(10, 0, 0))
    lineTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(5 ,4, 0),
                                                             adsk.core.Point3D.create(19, 13, 0))
    firstLinePoint = adsk.core.Point3D.create(3, 0, 0)
    secondLinePoint = adsk.core.Point3D.create(5, 4, 0)
    distance = 2.0
    angle = 0.610865

    # Create the chamfer between the two lines
    chamfer = sketch.sketchCurves.sketchLines
    angleChamfer = chamfer.addAngleChamfer(lineOne, firstLinePoint, lineTwo, secondLinePoint, distance, angle)
```

