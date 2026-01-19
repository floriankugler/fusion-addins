# baseFeatures.add

## Description

Demonstrates the baseFeature.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_baseFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    baseFeatures = rootComp.features.baseFeatures
    baseFeature = baseFeatures.add()
```

