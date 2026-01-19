# AutoConstrain Sample

## Description

Demonstrates using the AutoConstrain API to automatically add geometric constraints and dimensions to a sketch. This sample creates a simple sketch with a rectangle and circle, then applies automatic constraints using the origin point as a datum.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create a new document
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        
        # Create a sketch on XY plane
        sketches = rootComp.sketches
        sketch = sketches.add(rootComp.xYConstructionPlane)
        
        # Create simple geometry: Rectangle + Circle
        sketchLines = sketch.sketchCurves.sketchLines
        rectangleLines = sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(10, 5, 0)
        )
        
        circles = sketch.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(
            adsk.core.Point3D.create(5, 2.5, 0),
            2
        )
        
        # Create AutoConstrainInput
        autoConstrainInput = sketch.createAutoConstrainInput()
        
        # Set the origin point as datum
        originPoint = sketch.originPoint
        autoConstrainInput.datumPoint = originPoint
        
        # Execute autoConstrain
        result = sketch.autoConstrain(autoConstrainInput)
        
        # Get results
        addedConstraints = len(result.addedConstraints)
        addedDimensions = len(result.addedDimensions)
        isFullyConstrained = result.isFullyConstrained
        
        # Log AutoConstrain results
        app.log(f'AutoConstrain Results:')
        app.log(f'  Datum Point: Origin')
        app.log(f'  Added Constraints: {addedConstraints}')
        app.log(f'  Added Dimensions: {addedDimensions}')
        app.log(f'  Is Fully Constrained: {isFullyConstrained}')
        
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

