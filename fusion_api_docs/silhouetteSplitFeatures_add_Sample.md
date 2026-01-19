# silhouetteSplitFeatures.add

## Description

Demonstrates the silhouetteSplitFeatures.add method. The Silhouette Split feature is limited in the bodies it will split. The simplest body to get a valid result is to create a sphere and split it.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_silhouetteSplitFeatures_add(rootComp: adsk.fusion.Component):
    body = _ui.selectEntity('Select a body', 'Bodies').entity

    viewDirection = rootComp.zConstructionAxis
    operation = adsk.fusion.SilhouetteSplitOperations.SilhouetteSplitSolidBodyOperation
    silhouetteSplitFeatures = rootComp.features.silhouetteSplitFeatures
    input = silhouetteSplitFeatures.createInput(viewDirection, body, operation)
    silhouetteSplitFeature = silhouetteSplitFeatures.add(input)
```

