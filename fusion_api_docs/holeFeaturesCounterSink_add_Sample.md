# holeFeatures.add with Countersink

## Description

Demonstrates the holeFeatures.add method using the createCountersinkInput method and postions the hole in the center of a selected circular edge.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_holeFeatures_add_countersink(rootComp: adsk.fusion.Design.rootComponent):
    # Have the face and edges selected.
    face: adsk.fusion.BRepFace = _ui.selectEntity('Select a face', 'Faces').entity
    circleEdge: adsk.fusion.BRepEdge = _ui.selectEntity('Select circular edge', 'CircularEdges').entity

    # Define the needed inputs.
    holeDiam = adsk.core.ValueInput.createByString('20 mm')
    holeDepth = adsk.core.ValueInput.createByReal(5)
    countersinkDiam = adsk.core.ValueInput.createByString('35 mm')
    countersinkAngle = adsk.core.ValueInput.createByString('120 deg')

    holeFeatures: adsk.fusion.HoleFeatures = rootComp.features.holeFeatures
    input = holeFeatures.createCountersinkInput(holeDiam, countersinkDiam, countersinkAngle)
    input.setDistanceExtent(holeDepth)
    input.setPositionAtCenter(face, circleEdge)
    holeFeature = holeFeatures.add(input)
```

