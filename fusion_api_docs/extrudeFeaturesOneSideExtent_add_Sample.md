# extrudeFeatures.add using setOneSideExtent

## Description

Demonstrates the extrudeFeatures.add method using the setOneSideExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeaturesOneSideExtent_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have profile selected.
    profile = _ui.selectEntity('Select a profile', 'Profiles').entity

    # Define the required input.
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    extrudeFeatures = rootComp.features.extrudeFeatures
    input: adsk.fusion.ExtrudeFeatureInput = extrudeFeatures.createInput(profile, operation)

    distance = adsk.core.ValueInput.createByString('30 mm')
    distanceExtent = adsk.fusion.DistanceExtentDefinition.create(distance)
    direction = adsk.fusion.ExtentDirections.PositiveExtentDirection
    input.setOneSideExtent(distanceExtent, direction)

    # Create the feature.
    extrudeFeature = extrudeFeatures.add(input)
```

