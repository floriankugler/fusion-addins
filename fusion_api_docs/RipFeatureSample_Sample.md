# Rip Feature Sample

## Description

Demonstrates creating a new sheet metal rip feature.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
       
        # get active design        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
         
        # get the root component
        rootComp = design.rootComponent

        # get features
        features = rootComp.features
        ripFeatures = features.ripFeatures

        # get geometry from body to create a rip
        brepBodies = rootComp.bRepBodies
        body = brepBodies.item(0)
        edges = body.edges
        vertices = body.vertices

        # create a between points rip
        gapDistance = adsk.core.ValueInput.createByReal(1.23)
        offset1 = adsk.core.ValueInput.createByReal(2.34)
        ripFeatureInput = ripFeatures.createRipFeatureInput()
        edge = edges.item(40)
        vertex = vertices.item(9)
        ripFeatureInput.setBetweenPoints(edge, vertex, gapDistance, offset1)
        ripFeature = ripFeatures.add(ripFeatureInput)
           
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

