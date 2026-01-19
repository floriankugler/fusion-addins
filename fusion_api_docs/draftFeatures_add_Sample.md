# draftFeatures.add

## Description

Demonstrates the draftFeatures.add method. To use this sample, have a design open that contains at least one body. When you run the sample, you will be prompted to select the face to draft. Because the pull direction is using the base X-Y plane, you need to select a face that is not parallel to the X-Y plane.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_draftFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the face to draft selected and add it to a list.
    face = _ui.selectEntity('Select a face to draft', 'Faces').entity
    faces = []
    faces.append(face)

    # Define the pull direction and angle.
    pullDirection = rootComp.xYConstructionPlane
    angle = adsk.core.ValueInput.createByString("30 deg")

    # Define the required input and create the draft feature.
    draftFeatures = rootComp.features.draftFeatures
    input = draftFeatures.createInput(faces, pullDirection)
    input.setSingleAngle(True, angle)
    draftFeature = draftFeatures.add(input)
```

