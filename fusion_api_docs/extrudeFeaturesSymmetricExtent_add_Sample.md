# extrudeFeatures.add using setSymmetricExtent

## Description

Demonstrates the extrudeFeatures.add method using the setSymmetricExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeaturesSymmetricExtent_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have a profile selected.
    profile = _ui.selectEntity('Select a profile', 'Profiles').entity

    # Define the required input.
    extrudeFeatures = rootComp.features.extrudeFeatures
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    input = extrudeFeatures.createInput(profile, operation)
    distance = adsk.core.ValueInput.createByString("100 mm")
    isFullLength = True
    input.setSymmetricExtent(distance, isFullLength)

    # Create the feature.
    extrudeFeature = extrudeFeatures.add(input)
```

