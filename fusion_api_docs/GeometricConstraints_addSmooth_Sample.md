# GeometricConstraints.addSmooth

## Description

Demonstrate the GeometricConstraints.addSmooth method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_GeometricConstraints_addSmooth(sketch: adsk.fusion.Sketch):
    # Create a sketch arc.
    arc = sketch.sketchCurves.sketchArcs.addByCenterStartSweep(adsk.core.Point3D.create(5, 5, 0),
                                                               adsk.core.Point3D.create(15, 0, 0),
                                                               -135.0)

    # Create a spline that's connected to the end point of the arc.
    points = adsk.core.ObjectCollection.create()
    points.add(arc.endSketchPoint)
    points.add(adsk.core.Point3D.create(10, 8, 0))
    points.add(adsk.core.Point3D.create(5, 6, 0))
    points.add(adsk.core.Point3D.create(0, 8, 0))
    spline = sketch.sketchCurves.sketchFittedSplines.add(points)
    
    # Create the smooth constraint between the arc and the spline.
    constraints = sketch.geometricConstraints
    smoothConstraint = constraints.addSmooth(arc, spline)
```

