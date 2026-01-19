# Hem Feature Sample

## Description

Demonstrates creating a new sheet metal hem feature.

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
        hemFeatures = features.hemFeatures

        # get geometry from body to create hems
        brepBodies = rootComp.bRepBodies
        body = brepBodies.item(0)
        edges = body.edges

        # get inputs for an open hem
        gap = adsk.core.ValueInput.createByReal(0.2)
        length = adsk.core.ValueInput.createByReal(2.0)
        openHemFeatureInput = hemFeatures.createHemFeatureInput()
        edge = edges.item(0)
        isFlipped = False
        bendPositionType = adsk.fusion.BendPositionTypes.StartEdgeBendPositionType;

        # create an open hem using specified values
        openHemFeatureInput.setOpenHem(edge, length, gap, isFlipped, bendPositionType)
        hemFeature = hemFeatures.add(openHemFeatureInput)

        # get inputs for a rolled hem
        radius = adsk.core.ValueInput.createByReal(0.3)
        angle = adsk.core.ValueInput.createByReal(4.5)
        rolledHemFeatureInput = hemFeatures.createHemFeatureInput()
        edge = edges.item(5)

        # use same flip and bend position as before to create a rolled hem
        rolledHemFeatureInput.setRolledHem(edge, radius, angle, isFlipped, bendPositionType)
        hemFeature = hemFeatures.add(rolledHemFeatureInput)
           
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

