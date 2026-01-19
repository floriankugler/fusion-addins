# Create Animation API Sample

## Description

Creates a series of images of a design where a parameter is being changed. The series of images can be used to create an animation using other software. To run this sample, have a part open that contains a parameter named "Length". The parameter should be able to be successfully modified from 10 to 15 centimeters. Run the sample and choose or create a directory for the output. After running you should have a folder full of images that are snapshots of each parameter value.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, traceback
import os

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface        
        des = adsk.fusion.Design.cast(app.activeProduct)

        paramName = 'Length'
        startValue = 10
        endValue = 15
        increment = .1

        # Get the output folder.
        fd = ui.createFolderDialog()
        fd.title = "Specify Output Folder"
        if fd.showDialog() != adsk.core.DialogResults.DialogOK:
            return

        resultFolder = fd.folder

        param = des.allParameters.itemByName(paramName)
        if not param:
            ui.messageBox('The parameter "' + paramName + '" must exist.')
            return

        currentValue = startValue
        param.value = currentValue

        # Iterate from the start to end values, capturing a screen 
        # for each one.        
        cnt = 0
        while param.value < endValue:
            param.value = currentValue
            currentValue += increment
            adsk.doEvents()
            filename = os.path.join(resultFolder, "frame" + str(cnt).zfill(4))
            app.activeViewport.saveAsImageFile(filename, 0, 0)                
            cnt += 1
            
        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

