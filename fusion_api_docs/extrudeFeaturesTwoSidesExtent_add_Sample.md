# extrudeFeatures.add using setTwoSidesExtent

## Description

Demonstrates the extrudeFeatures.add method using the setTwoSidesExtent method. To use this sample have a design open that contains a profile and a body that is positioned away from the profile but is a size where when the profile is extruded it will intersect the body. When you run the script you will be prompted to select the profile that will be used to create the extrusion and the body to extrude to. The extrusion will be created up to the body with an offset and will also be offset from the sketch plane.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extrudeFeaturesTwoSidesExtent_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the profile and body selected.
    profile = _ui.selectEntity('Select a profile', 'Profiles').entity
    body = _ui.selectEntity('Select body to extrude to', 'Bodies').entity

    # Create a ToEntityExtentDefinition to define how the extrude will go up to the body.
    offset = adsk.core.ValueInput.createByString("2 mm")
    isChained = True
    sideOne = adsk.fusion.ToEntityExtentDefinition.create(body, isChained, offset)

    # Create a DistanceExtentDefinition ot define how the extrude will go a specific distance.
    distance = adsk.core.ValueInput.createByString("5 mm")
    sideTwo = adsk.fusion.DistanceExtentDefinition.create(distance)

    # Create the extrude input with extents to two sides.
    extrudeFeatures = rootComp.features.extrudeFeatures
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    input = extrudeFeatures.createInput(profile, operation)
    input.setTwoSidesExtent(sideOne, sideTwo)

    # Create the extrude feature.
    extrudeFeature = extrudeFeatures.add(input)
```

