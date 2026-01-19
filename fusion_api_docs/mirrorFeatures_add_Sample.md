# mirrorFeatures.add

## Description

Demonstrates the mirrorFeatures.add method by mirroring the selected body around the base X-Y construction plane.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_mirrorFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    body = _ui.selectEntity('Select the body to mirror', 'Bodies').entity
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)

    mirrorFeatures = rootComp.features.mirrorFeatures
    mirrorPlane = rootComp.xYConstructionPlane
    mirrorInput = mirrorFeatures.createInput(bodies, mirrorPlane)
    mirrorFeature = mirrorFeatures.add(mirrorInput)
```

