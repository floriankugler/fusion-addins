# Create CAM Operation From Template API Sample

## Description

Demonstrates adding a new toolpath into the document using an existing CAM template. You can view the template [here](../ExtraFiles/face.f3dhsm-template), although it will be loaded automatically. Run the sample script within any Fusion project containing at least one setup. A new facing operation will be created at the end of each setup discovered.

## Code Samples

| Copy Code |
|----------:|

```python
# Apply a CAM Template to a specific machining operation on the selected model of each setup.

import adsk.core, adsk.fusion, adsk.cam, os, traceback

# The location from where a sample template file can be downloaded if performed manually.
TEMPLATE_URL = 'https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/ExtraFiles/face.f3dhsm-template'

# The name of the template file.
TEMPLATE_FILE = 'face.f3dhsm-template'

# The URN is the identifier of the template as located within Fusion's library of sample templates.
TEMPLATE_URN = 'urn:adsk.wipprod:fs.file:vf.p0C9h2KARa61iM_vsZauog?version=1'

# Variable initialisation.
app = adsk.core.Application.get()
ui = app.userInterface
doc = app.activeDocument

def abandonScript(notice:str):
    notice += '\nAfter completing the above tasks, run this script again.'
    # Spaces appended to the title make the messageBox wider, preventing line wrapping.
    ui.messageBox(
        notice,
        'Please take note of the following:\t\t\t\t',
        adsk.core.MessageBoxButtonTypes.OKButtonType,
        adsk.core.MessageBoxIconTypes.WarningIconType)

def run(context):

    # Variable initialisation.
    notice = ''
    occurrenceCount = 0
    bRepBodyCount = 0
    
    try:
        # Switch to manufacturing space.
        camWS = ui.workspaces.itemById('CAMEnvironment') 
        camWS.activate()

        # Get the CAM product.
        products = doc.products
        cam: adsk.cam.CAM = products.itemByProductType('CAMProductType')

        # Get the CAD product.
        design: adsk.fusion.Design = products.itemByProductType('DesignProductType')
        
        # An alternative possibility.
        if not design:
            design = products.itemByProductType('WorkingModelProductType')
        
        # Check that a model exists in this document.
        if design:
            occurrenceCount  = design.rootComponent.occurrences.count 
            bRepBodyCount = design.rootComponent.bRepBodies.count
        else:
            notice += 'No active Fusion design found.\n'

        if bRepBodyCount  0):
            abandonScript(notice)
            return

        # We are unable to read the content of a CAMTemplate dataFile directly from its URN.
        # Instead we download the dataFile from the URN into a temporary folder and read the file contents.

        # Set CAM temporary folder as inputFolder.
        # Variable inputFolder may contain backslashes but we need forward slashes.
        inputFolder = str(cam.temporaryFolder).replace('\\', '/') 

        # Specify the full filename of the template.
        templatePathname = f'{inputFolder}/{TEMPLATE_FILE}'

        # Check if the template exists (from the path specified above). Show an error if it fails to download.
        if not os.path.exists(templatePathname):
            templateDataFile: adsk.core.DataFile = None
            try:
                templateDataFile = app.data.findFileById(TEMPLATE_URN)
            except:
                notice += f'\nUnable to locate template via {TEMPLATE_URN}.\n'

            downloadSuccess:bool = False
            if templateDataFile:
                try:
                    downloadSuccess = templateDataFile.download(templatePathname, None)
                except Exception as e:
                    notice += f'\n{e}\n'
            
            if not downloadSuccess:
                # We should never get here but if so, explain how to perform the previous step manually.
                notice += f'\nThe template file: {TEMPLATE_FILE} has not been found.\n'
                notice += f'\nCreate your own template file called {TEMPLATE_FILE} '
                notice += f'or download a sample file from here:\n\n{TEMPLATE_URL}\n\n'
                notice += f'Move the downloaded template file to this folder:\n\n{inputFolder}\n\n'

        # Present a single messageBox stating problems, remedies and instructions.
        if len(notice) > 0:
            abandonScript(notice)
            return
        
        # Go through each setup in the document.
        for setup in setups:
            # Add a templated operation to each setup.
            templateInput = adsk.cam.CreateFromCAMTemplateInput.create()
            camTemplate = adsk.cam.CAMTemplate.createFromFile(templatePathname)
            templateInput.camTemplate = camTemplate
            results: list[adsk.cam.OperationBase] = setup.createFromCAMTemplate2(templateInput)

            # Get the operation that was created. What's created will vary depending on what's defined 
            # in the template so you may need more logic to find the result you want.
            operation: adsk.cam.OperationBase = results[0]

            # Change the operation name.
            name = operation.name + ' (API added operation)'
            operation.name = name

            # Make the toolpath visible.
            operation.isSuppressed = False
            operation.isLightBulbOn = True
        
        # Generate all toolpaths, skipping any that are already valid.
        cam.generateAllToolpaths(True)

        # Indicate what has changed within the setup.
        notice = 'Expand the setup to see all operations.\n\n'
        notice += 'Note the operation names appended with: (API added operation).'
        ui.messageBox(
            notice,
            'Operation creation from template complete.\t\t',
            adsk.core.MessageBoxButtonTypes.OKButtonType, 
            adsk.core.MessageBoxIconTypes.InformationIconType)

    # Capture and highlight any reason for error
    except Exception as e:
        if ui:
            ui.messageBox(
                f'Failed: {e}\n{format(traceback.format_exc())}',
                'Unable to continue',
                adsk.core.MessageBoxButtonTypes.OKButtonType, 
                adsk.core.MessageBoxIconTypes.CriticalIconType)
```

