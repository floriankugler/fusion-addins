# moveFeatures.add

## Description

Demonstrates the moveFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_moveFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the body to move selected.
    selection = _ui.selectEntity('Select a body', 'Bodies').entity
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(selection)

    # Define a matrix that will move the body 10 cm in the Y direction.
    vector = adsk.core.Vector3D.create(0.0, 10.0, 0.0)
    transform = adsk.core.Matrix3D.create()
    transform.translation = vector

    moveFeatures = rootComp.features.moveFeatures
    input = moveFeatures.createInput2(bodies, transform)
    input.defineAsFreeMove(transform)
    moveFeature = moveFeatures.add(input)
```

