# revolveFeatures.add

## Description

Demonstrates creating a revolve feature using an angle extent.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_revolveFeatures_add(rootComp: adsk.fusion.Component):
    profile = _ui.selectEntity('Select a profile to revolve.', 'Profiles').entity
    axis = _ui.selectEntity('Select sketch line for axis.', 'SketchLines').entity
    operation = adsk.fusion.FeatureOperations.NewComponentFeatureOperation

    revolveFeatures = rootComp.features.revolveFeatures
    input = revolveFeatures.createInput(profile, axis, operation)
    input.setAngleExtent(False, adsk.core.ValueInput.createByString('90 deg'))
    revolveFeature = revolveFeatures.add(input)
```

