# scaleFeatures.add

## Description

Demonstrates the creation a scale feature.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_scaleFeatures_add(rootComp: adsk.fusion.Component):
    body = _ui.selectEntity('Select a body', 'Bodies').entity
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)
    scalePoint: adsk.fusion.BRepVertex = _ui.selectEntity('Select a vertex as the scale origin.', 'Vertices').entity
    scaleFactor = adsk.core.ValueInput.createByReal(0.5)

    scaleFeatures = rootComp.features.scaleFeatures
    input = scaleFeatures.createInput(bodies, scalePoint, scaleFactor)
    scaleFeature = scaleFeatures.add(input)
```

