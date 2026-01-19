# shellFeatures.add

## Description

Demonstrates creating a shell feature.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_shellFeatures_add(rootComp: adsk.fusion.Component):
    face = _ui.selectEntity('Select a face to open as part of a shell feature.', 'Faces').entity
    bodiesAndFaces = adsk.core.ObjectCollection.create()
    bodiesAndFaces.add(face)

    shellFeatures = rootComp.features.shellFeatures
    input: adsk.fusion.ShellFeatureInput = shellFeatures.createInput(bodiesAndFaces, True)
    input.insideThickness = adsk.core.ValueInput.createByReal(0.25)
    shellFeature = shellFeatures.add(input)
```

