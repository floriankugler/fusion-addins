# Sheet Metal Rules Sample

## Description

Demonstrates creating adding a sheet metal rule.

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
       
        # Create a document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        # get active design and components
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the sheet metal rules
        sheetMetalRules = design.librarySheetMetalRules

        # Get the steel (default) rule then create a copy of it
        steelRule = sheetMetalRules.item(0)
        steelCopy = sheetMetalRules.addByCopy(steelRule, 'Steel Two (mm)')

        # Make some changes to the copied rule
        # First we can make some direct changes
        steelCopy.kFactor = 0.5
        steelCopy.twoBendReliefShape = adsk.fusion.TwoBendReliefShapes.RoundTwoBendReliefShape
        steelCopy.twoBendReliefPlacement = adsk.fusion.TwoBendReliefPlacements.TangentTwoBendReliefPlacement

        # Some changes need to be changed by value and can't be made directly on the rule
        thicknessValue = steelCopy.thickness
        thicknessValue.value = 0.02
        gapValue = steelCopy.gap
        gapValue.value = 0.03

        # You can also delete rules, create a test and delete it
        ruleToDelete = sheetMetalRules.addByCopy(steelCopy, 'Steel Three (mm)')
        ruleToDelete.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

