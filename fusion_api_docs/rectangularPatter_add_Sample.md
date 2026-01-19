# rectangularPattern.add

## Description

Demonstrates the rectangularPattern.add method using a selected body and two selected edges to define the directions.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_rectangularPatternFeatures_add(rootComp: adsk.fusion.Component):
    body = _ui.selectEntity('Select a body to pattern.', 'Bodies').entity
    directionEdgeOne = _ui.selectEntity('Select direction edge one.', 'LinearEdges').entity
    directionEdgeTwo = _ui.selectEntity('Select direction edge two.', 'LinearEdges').entity

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)
    quantityOne = adsk.core.ValueInput.createByReal(4)
    distanceOne = adsk.core.ValueInput.createByReal(5)
    quantityTwo = adsk.core.ValueInput.createByReal(3)
    distanceTwo = adsk.core.ValueInput.createByReal(4)
    patternDistance = adsk.fusion.PatternDistanceType.SpacingPatternDistanceType

    rectangularPatterns = rootComp.features.rectangularPatternFeatures
    input = rectangularPatterns.createInput(bodies, directionEdgeOne, quantityOne, distanceOne, patternDistance)
    input.setDirectionTwo(directionEdgeTwo, quantityTwo, distanceTwo)
    rectangularPattern = rectangularPatterns.add(input)
```

