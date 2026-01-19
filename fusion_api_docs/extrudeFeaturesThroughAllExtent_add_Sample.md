# extrudeFeatures.add using ThroughAllExtent

## Description

Demonstrates the extrudeFeatures.add method using the ThroughAllExtent method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeaturesThroughAllExtent_add(rootComp: adsk.fusion.Design.rootComponent):
    filter =  adsk.core.SelectionCommandInput.Profiles
    profile = _ui.selectEntity('Select a profile', filter).entity
    operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    thruAllExtent = adsk.fusion.ThroughAllExtentDefinition.create()

    extrudeFeatures: adsk.fusion.ExtrudeFeatures = rootComp.features.extrudeFeatures
    input = extrudeFeatures.createInput(profile, operation)
    # You may need to change this to PositiveExtentDirection depending on your model.
    input.setOneSideExtent(thruAllExtent, adsk.fusion.ExtentDirections.NegativeExtentDirection)
    extrudeFeature = extrudeFeatures.add(input)
```

