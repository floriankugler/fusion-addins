# extrudeFeatures.add using thin extrude

## Description

Demonstrates the extrudeFeatures.add method using the setThinExtrude method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the thin extrusion.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeaturesThin_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the profile selected.
    filter =  adsk.core.SelectionCommandInput.Profiles
    profile = _ui.selectEntity('Select a profile', filter).entity

    # Define the required input.
    extrudeFeatures = rootComp.features.extrudeFeatures
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    input = extrudeFeatures.createInput(profile, operation)
    wallLocation = adsk.fusion.ThinExtrudeWallLocation.Center
    wallThickness = adsk.core.ValueInput.createByString("2 mm")
    input.setThinExtrude(wallLocation, wallThickness)
    distance = adsk.core.ValueInput.createByString("100 mm")
    isFullLength = True
    input.setSymmetricExtent(distance, isFullLength)

    # Create the feature.
    extrudeFeature = extrudeFeatures.add(input)
```

