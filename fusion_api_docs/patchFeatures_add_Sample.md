# patchFeatures.add

## Description

Demonstrates the patchFeatures.add method by creating a patch surface on the selected profile.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_patchFeatures_add(comp: adsk.fusion.Component):
    profile = _ui.selectEntity('Select a profile', 'Profiles').entity
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

    patchFeatures = comp.features.patchFeatures
    input = patchFeatures.createInput(profile, operation)
    patchFeature = patchFeatures.add(input)
```

