# combineFeatures.add

## Description

Demonstrates the combineFeatures.add method. To use this sample, have a design open that contains at least two bodies. When you run the sample, you will be prompted to select the bodies and they will joined.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_combineFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the two bodies selected.
    targetBody = _ui.selectEntity('Select a body', 'Bodies').entity
    toolBody = _ui.selectEntity('Select Bodies', 'Bodies').entity

    # Define the required inputs and create te combine feature.
    combineFeatures = rootComp.features.combineFeatures
    tools = adsk.core.ObjectCollection.create()
    tools.add(toolBody)
    input: adsk.fusion.CombineFeatureInput = combineFeatures.createInput(targetBody, tools)
    input.isNewComponent = False
    input.isKeepToolBodies = False
    input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combineFeature = combineFeatures.add(input)
```

