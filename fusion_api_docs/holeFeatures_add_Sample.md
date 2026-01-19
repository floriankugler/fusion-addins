# holeFeatures.add

## Description

Demonstrates the holeFeatures.add method using the createSimpleInput method. To use this sample, have a design open with a box. Select the face for the hole and two edges to define the position of the hole.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_holeFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the face and edges selected.
    face: adsk.fusion.BRepFace = _ui.selectEntity('Select a face', 'Faces').entity
    edge1: adsk.fusion.BRepEdge = _ui.selectEntity('Select edge 1', 'Edges').entity
    edge2: adsk.fusion.BRepEdge = _ui.selectEntity('Select edge 2', 'Edges').entity

    # Define the needed inputs.
    holeDiam = adsk.core.ValueInput.createByString('20 mm')
    holeDepth = adsk.core.ValueInput.createByReal(5)
    offset1 = adsk.core.ValueInput.createByReal(4)
    offset2 = adsk.core.ValueInput.createByReal(6)

    holeFeatures: adsk.fusion.HoleFeatures = rootComp.features.holeFeatures

    # Define as a plain hole.
    input = holeFeatures.createSimpleInput(holeDiam)
    input.setDistanceExtent(holeDepth)
    facePoint = face.pointOnFace
    input.setPositionByPlaneAndOffsets(face, facePoint, edge1, offset1, edge2, offset2)
    holeFeature = holeFeatures.add(input)
```

