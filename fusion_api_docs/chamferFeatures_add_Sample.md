# chamferFeatures.add

## Description

Demonstrates the chamferFeatures.add method. To use this sample have a part open that contains a body. When you run the script, you will be prompted to select an edge to chamfer.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_chamferFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    selection = _ui.selectEntity('Select edge to chamfer', 'Edges')
    edge : adsk.fusion.BRepEdge = selection.entity
    edgeCollection = adsk.core.ObjectCollection.create()
    edgeCollection.add(edge)

    chamfers = rootComp.features.chamferFeatures
    input = chamfers.createInput2()
    offset = adsk.core.ValueInput.createByReal(1)
    input.chamferEdgeSets.addEqualDistanceChamferEdgeSet(edgeCollection, offset, True)

    # Create the chamfer
    chamfer = chamfers.add(input)
```

