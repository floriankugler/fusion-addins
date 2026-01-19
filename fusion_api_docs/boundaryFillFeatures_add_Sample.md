# boundaryFillFeatures.add

## Description

Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_boundaryFillFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the two bodies selected.
    filter = adsk.core.SelectionCommandInput.Bodies
    body1 = _ui.selectEntity('Select tool body 1', filter).entity
    body2 = _ui.selectEntity('Select tool body 2', filter).entity

    # Create an ObjectCollection to use the bodies as tools.
    tools = adsk.core.ObjectCollection.create()
    tools.add(body1)
    tools.add(body2)

    # Create the input object to provide the required input.
    boundaryFills = rootComp.features.boundaryFillFeatures
    input = boundaryFills.createInput(tools, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Arbitrarily specify the first volume as selected.
    input.bRepCells.item(0).isSelected = True  

    # Create the boundary fill feature.
    boundaryFill = boundaryFills.add(input)
```

