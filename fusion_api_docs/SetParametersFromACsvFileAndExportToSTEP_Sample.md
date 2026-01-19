# Set parameters from a csv file and export to STEP

## Description

Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model.

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
        
        design = app.activeProduct
        # Read the csv file.
        cnt = 0
        file = open('C://Temp//values.csv')
        for line in file:
            # Get the values from the csv file.
            pieces = line.split(',')
            
            length = pieces[0]
            width = pieces[1]
            height = pieces[2]
            
            # Set the parameters.
            lengthParam = design.userParameters.itemByName('Length')
            lengthParam.expression = length
            
            widthParam = design.userParameters.itemByName('Width')
            widthParam.expression = width

            heightParam = design.userParameters.itemByName('Height')
            heightParam.expression = height
            
            #Export the STEP file.
            exportMgr = design.exportManager
            stepOptions = exportMgr.createSTEPExportOptions('C:\\Temp\\test_​box' + str(cnt) + '.stp')
            cnt += 1
            res = exportMgr.execute(stepOptions)
        
        ui.messageBox('Finished')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

