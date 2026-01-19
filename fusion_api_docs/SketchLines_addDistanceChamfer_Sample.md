# SketchLines.addDistanceChamfer

## Description

Demonstrates the SketchLines.addDistanceChamfer method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_Lines_addDistanceChamfer(sketch: adsk.fusion.Sketch):
    # Create lines that will be chamfered
    lineOne = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0),
                                                             adsk.core.Point3D.create(10, 0, 0))
    lineTwo = sketch.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(5, 4, 0),
                                                             adsk.core.Point3D.create(19, 13, 0))

    # Define the input parameters.
    firstLinePoint = adsk.core.Point3D.create(3, 0, 0)
    secondLinePoint = adsk.core.Point3D.create(5, 4, 0)
    distanceOne = 2.0
    distanceTwo = 5.0 

    # Create the chamfer between the two lines
    chamfer = sketch.sketchCurves.sketchLines
    distanceChamfer = chamfer.addDistanceChamfer(lineOne, firstLinePoint, lineTwo, secondLinePoint, distanceOne, distanceTwo)
```

