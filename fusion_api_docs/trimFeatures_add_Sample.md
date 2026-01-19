# trimFeatures.add

## Description

Demonstrates the trimFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_trimFeatures_add(rootComp: adsk.fusion.Component):
    tool = _ui.selectEntity('Select trimming tool', 'SketchCurves').entity

    trimFeatures = rootComp.features.trimFeatures
    input = trimFeatures.createInput(tool)

    # Arbitrarily choose the first cell to trim.
    cells = input.bRepCells
    cells[0].isSelected = True

    # Create the feature.
    trimFeatures.add(input)
```

