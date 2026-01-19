# Get Volume of Active Design API Sample

## Description

Traverses through the active design and totals the volume of every body within the design.

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
        
        design = app.activeProduct
        if not design:
            ui.messageBox('No active Fusion design', 'No Design')
            return

        # Get the root component of the active design.
        rootComp = design.rootComponent
        
        # Iterate over any bodies in the root component.
        totalVolume = 0
        for j in range(0, rootComp.bRepBodies.count):
            body = rootComp.bRepBodies.item(j)

            # Get the volume of the current body and add it to the total.
            totalVolume += body.volume

        # Iterate through all of the occurrences in the assembly.
        for i in range(0, rootComp.allOccurrences.count):
            occ = rootComp.allOccurrences.item(i)
            
            # Get the associated component.
            comp = occ.component
            
            # Iterate over all of the bodies within the component.
            for j in range(0, comp.bRepBodies.count):
                body = comp.bRepBodies.item(j)
                
                # Get the volume of the current body and add it to the total.
                totalVolume += body.volume
        
        # Format a string to display the volume using the default distance units.
        result = design.unitsManager.formatValue(totalVolume, design.unitsManager.defaultLengthUnits + '^3')
        ui.messageBox('The volume of the entire asembly is: ' + result)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

