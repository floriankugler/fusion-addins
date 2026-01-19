# sweepFeatures.add

## Description

Demonstrates the sweepFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_sweepFeatures_add(rootComp: adsk.fusion.Component):
    profile = _ui.selectEntity('Select a profile.', 'Profiles').entity
    pathCurve = _ui.selectEntity('Select a path curve', 'SketchCurves').entity

    path = adsk.fusion.Path.create(pathCurve, adsk.fusion.ChainedCurveOptions.tangentChainedCurves)

    sweepFeatures = rootComp.features.sweepFeatures
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    input = sweepFeatures.createInput(profile, path, operation)
    input.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    sweepFeature = sweepFeatures.add(input)
```

