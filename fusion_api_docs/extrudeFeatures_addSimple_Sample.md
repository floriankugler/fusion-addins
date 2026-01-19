# extrudeFeatures.addSimple

## Description

Demonstrates the extrudeFeatures.addSimple method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeatures_addSimple(rootComp: adsk.fusion.Design.rootComponent):
    filter =  adsk.core.SelectionCommandInput.Profiles
    profile = _ui.selectEntity('Select a profile', filter).entity
    distance = adsk.core.ValueInput.createByString("100 mm")
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

    extrudeFeatures = rootComp.features.extrudeFeatures
    extrudeFeature = extrudeFeatures.addSimple(profile, distance, operation)
```

