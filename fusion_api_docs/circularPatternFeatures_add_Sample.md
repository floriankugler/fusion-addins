# circularPatternFeatures.add

## Description

Demonstrates the circularPatternFeatures.add method. To use the sample have a design open that contains at least one body. When you run the script, it will prompt you to select a body, which will be patterned around the base Y-axis.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_circularPatternFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the body to be pattern selected and add it to a collection.
    selectedBody = _ui.selectEntity('Select a body', 'Bodies').entity
    inputEntities = adsk.core.ObjectCollection.create()
    inputEntities.add(selectedBody)

    # Define the required inputs and create the feature.
    circularFeats = rootComp.features.circularPatternFeatures
    yAxis: adsk.core.Base = rootComp.yConstructionAxis
    circularFeatInput = circularFeats.createInput(inputEntities, yAxis)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(5)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('180 deg')
    circularFeatInput.isSymmetric = False
    circularFeat = circularFeats.add(circularFeatInput)
```

