# holeFeatures.add with Counterbore

## Description

Demonstrates the holeFeatures.add method using the createCounterboreInput method. The hole is positioned at the center of the selected edge.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_holeFeatures_add_counterbore(rootComp: adsk.fusion.Design.rootComponent):
    # Have the face and edges selected.
    face: adsk.fusion.BRepFace = _ui.selectEntity('Select a face', 'Faces').entity
    edge: adsk.fusion.BRepEdge = _ui.selectEntity('Select edge', 'Edges').entity

    # Define the needed inputs.
    holeDiam = adsk.core.ValueInput.createByString('10 mm')
    holeDepth = adsk.core.ValueInput.createByReal(5)
    counterboreDiam = adsk.core.ValueInput.createByString('20 mm')
    counterboreDepth = adsk.core.ValueInput.createByString('3 mm')
    offset1 = adsk.core.ValueInput.createByReal(4)
    offset2 = adsk.core.ValueInput.createByReal(6)

    holeFeatures: adsk.fusion.HoleFeatures = rootComp.features.holeFeatures
    input = holeFeatures.createCounterboreInput(holeDiam, counterboreDiam, counterboreDepth)
    input.setDistanceExtent(holeDepth)
    facePoint = face.pointOnFace
    input.setPositionOnEdge(face, edge, adsk.fusion.HoleEdgePositions.EdgeMidPointPosition)
    holeFeature = holeFeatures.add(input)
```

