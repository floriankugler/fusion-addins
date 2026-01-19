# splitBodyFeatures.add

## Description

Demonstrates the splitBodyFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_splitBodyFeatures_add(rootComp: adsk.fusion.Component):
    body = _ui.selectEntity('Select a body', 'Bodies').entity
    splittingTool = _ui.selectEntity('Select a face to split the body.', 'Bodies').entity
    isExtended = True

    splitBodyFeatures = rootComp.features.splitBodyFeatures
    input = splitBodyFeatures.createInput(body, splittingTool, isExtended)
    splitBodyFeature = splitBodyFeatures.add(input)
```

