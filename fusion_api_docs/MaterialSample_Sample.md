# Material API Sample

## Description

Demonstrates using materials and appearance using the API.

To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. The sample also used an external appearance library which you can get [here](../ExtraFiles/APISampleMaterialLibrary2.adsklib). Copy that to any location on your computer and edit the path in the script. When running the script, have a design open that contains a body in the root component.

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
        
        # Load a local material library. You'll need to edit the path to the libary.
        materialLibs = app.materialLibraries
        matLib = materialLibs.load('C:/Temp//APISampleMaterialLibrary2.adsklib')

        # Get the first appearance from the library.
        appear = matLib.appearances.item(0)

        # Copy the appearance into the design.
        des = adsk.fusion.Design.cast(app.activeProduct)             
        appear = des.appearances.addByCopy(appear, f'{appear.name}_Copied')
        
        # Apply the appearance to the first body in the design.
        root = des.rootComponent
        body = root.bRepBodies.item(0)
        body.appearance = appear
        
        # Unload the library.
        if matLib.isNative == False:
            matLib.unload()       
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

