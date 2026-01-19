# pathPatternFeatures.add

## Description

Demonstrates the pathPatternFeatures.add method using a selected body and sketch curve as the path.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_pathPatternFeatures_add(rootComp: adsk.fusion.Component):
    # Have the body to pattern and path curve selected.
    body = _ui.selectEntity('Select a body to pattern.', 'Bodies').entity
    path = adsk.fusion.Path.create(_ui.selectEntity('Select a curve', 'SketchCurves').entity, adsk.fusion.ChainedCurveOptions.tangentChainedCurves)

    # Define the required input.
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)
    quantity = adsk.core.ValueInput.createByReal(5)
    distance = adsk.core.ValueInput.createByReal(10)
    patternDistance = adsk.fusion.PatternDistanceType.SpacingPatternDistanceType
    
    patternFeatures = rootComp.features.pathPatternFeatures
    input = patternFeatures.createInput(bodies, path, quantity, distance, patternDistance)
    patternFeature = patternFeatures.add(input)
```

