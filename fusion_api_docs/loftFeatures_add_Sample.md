# loftFeatures.add

## Description

Demonstrates the loftFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_loftFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    profileOne: adsk.fusion.BRepFaces = _ui.selectEntity('Select a profile or face.', 'Profiles, Faces').entity
    profileTwo: adsk.fusion.BRepFaces = _ui.selectEntity('Select a profile or face', 'Profiles, Faces').entity

    # Define the needed input.
    loftFeatures = rootComp.features.loftFeatures
    input = loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftSections = input.loftSections
    loftSections.add(profileOne)
    loftSections.add(profileTwo)
    input.isSolid = True

    # Create the loft.
    loftFeature = loftFeatures.add(input)
```

