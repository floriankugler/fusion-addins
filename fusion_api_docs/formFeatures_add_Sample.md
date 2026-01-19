# formFeatures.add

## Description

Demonstrates the formFeatures.add method. This creates a new empty form (T-Spline) feature, which you'll see in the timeline.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_formFeatures_add(rootComp: adsk.fusion.Component):
    formFeatures: rootComp.features.formFeatures = rootComp.features.formFeatures
    formFeature = formFeatures.add()
```

