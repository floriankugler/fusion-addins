# stitchFeatures.add

## Description

Demonstrates the stitchFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_stitchFeatures_add(rootComp: adsk.fusion.Component):
    # Have the two bodies selected and add them to an ObjectCollection.
    body1: adsk.fusion.BRepBodies = _ui.selectEntity('Select a surface body.', 'Bodies').entity
    body2: adsk.fusion.BRepBodies = _ui.selectEntity('Select a connecting surface body.', 'Bodies').entity
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body1)
    bodies.add(body2)

    stitchFeatures = rootComp.features.stitchFeatures
    tolerance = adsk.core.ValueInput.createByReal(.01)
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    input = stitchFeatures.createInput(bodies, tolerance, operation)
    stitchFeature = stitchFeatures.add(input)
```

