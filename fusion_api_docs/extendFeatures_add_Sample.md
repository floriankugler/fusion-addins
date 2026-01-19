# extendFeatures.add

## Description

Demonstrates the extendFeatures.add method. To use this sample, have a design open that contains at least one surface body. When you run the sample, you will be prompted to select an open edge of the body.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_extendFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    # Have the edge to extend selected and add it to an ObjectCollection. 
    # This must be on a surface body and be an open edge or the creation 
    # of the feature will fail.
    edge: adsk.fusion.BRepEdge = _ui.selectEntity('Select edge to extend', 'Edges').entity
    edges = adsk.core.ObjectCollection.create()
    edges.add(edge)

    # Define the needed input.    
    distance = adsk.core.ValueInput.createByReal(5)
    extendType = adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType
    extendFeatures = rootComp.features.extendFeatures
    input: adsk.fusion.ExtendFeatureInput = extendFeatures.createInput(edges, distance, extendType)
    input.extendAlignment = adsk.fusion.SurfaceExtendAlignment.FreeEdges

    # Create the feature.
    extendFeature = extendFeatures.add(input)
```

