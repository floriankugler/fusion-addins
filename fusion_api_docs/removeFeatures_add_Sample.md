# removeFeatures.add

## Description

Demonstrate the removeFeatures.add method. The Remove feature is the same as selecting a body in the browser and selecting "Remove" in the context menu.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_removeFeatures_add(rootComp: adsk.fusion.Component):
    body = _ui.selectEntity('Select a body', 'Bodies').entity

    removeFeatures = rootComp.features.removeFeatures
    removeFeature = removeFeatures.add(body)
```

