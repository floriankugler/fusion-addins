# Additive Manufacturing MJF API Sample

## Description

Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer.

To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input.

The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback, tempfile, time

app = adsk.core.Application.get()
ui  = app.userInterface

# Global set of event handlers to keep them referenced for the duration of the command
handlers = []

def createManufacturingModel(cam: adsk.cam.CAM):
    showMessage('=============================================')
    showMessage('Creating Manufacturing Model...')
    manufacturingModels = cam.manufacturingModels
    mmInput = manufacturingModels.createInput()
    mmInput.name = "My Manufacturing Model - MJF"
    manufacturingModel = manufacturingModels.add(mmInput)

    showMessage('Getting occurrences...')
    occs = getValidOccurrences(manufacturingModel.occurrence)
    if len(occs) == 0:
        ui.messageBox('No component has been added to the scene.')
        return (None, [])
    
    return (manufacturingModel, occs)

# Create an additive setup.
def createAdditiveSetup(models: list[adsk.fusion.Occurrence], cam: adsk.cam.CAM, libraryManager: adsk.cam.CAMLibraryManager):
    showMessage('Creating Setup...')
    setups = cam.setups
    input = setups.createInput(adsk.cam.OperationTypes.AdditiveOperation)
    input.models = models
    input.name = 'AdditiveSetup'

    printSettingLibrary = libraryManager.printSettingLibrary
    machineLibrary = libraryManager.machineLibrary
    printSetting = None
    machine = None
    if True:
        # URL-structure browsing
        printSettingUrl = printSettingLibrary.urlByLocation(adsk.cam.LibraryLocations.Fusion360LibraryLocation) ## .Fusion360LibraryLocation vs .LocalLibraryLocation etc.
        printSettings = printSettingLibrary.childPrintSettings(printSettingUrl)

        machineUrl = machineLibrary.urlByLocation(adsk.cam.LibraryLocations.Fusion360LibraryLocation) ## .Fusion360LibraryLocation vs .LocalLibraryLocation etc.
        machines = machineLibrary.childMachines(machineUrl)
        for ps in printSettings:
            if ps.name ==  "HP - MJF": #print setting name from fusions library
                input.printSetting = ps
                break

        for machine in machines: #model name from fusions library
            if machine.model ==  "Jet Fusion 5200 Series":
                input.machine = machine
                break

    setup = setups.add(input)
    return setup

def createAdditiveArrange(setup: adsk.cam.Setup, cam: adsk.cam.CAM):
    # Define and create the arrange operation.
    showMessage('Generating Additive Arrange...')
    operationInput = setup.operations.createInput('additive_arrange')
    arrange = setup.operations.add(operationInput)

    parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_arrangement_type").value
    parameter.value = 'Pack3D_TrueShape'

    parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_priority_type").value
    parameter.value = 'priority_volume'

    parameter: adsk.cam.BooleanParameterValue = arrange.parameters.itemByName("arrange_quantity_group").value
    parameter.value = True
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_global_quantity").value
    parameter.value = 1
    
    parameter: adsk.cam.BooleanParameterValue = arrange.parameters.itemByName("arrange_rotation_group").value
    parameter.value = True

    parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_rotation_z").value
    parameter.value = 'arrange_rotation_90'

    parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_unselected_components_option").value
    parameter.value = 'unselected_move_outside'

    # Specify the values to control the arrangement. All length units are centimeters.
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_platform_clearance").value
    parameter.value = 0.0
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_frame_width").value
    parameter.value = 0.2
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_ceiling_clearance").value
    parameter.value = 0.2              

    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_object_spacing").value
    parameter.value = 0.5
   
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_voxelsize").value
    parameter.value = 0.5
    
    future = cam.generateToolpath(arrange)
    while (future.isGenerationCompleted == False):
        time.sleep(0.5)


# Event handler that reacts to when the command is executed.       
class MyCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Make sure the TEXT COMMAND palette is visible.
            textPalette = ui.palettes.itemById('TextCommands')
            if not textPalette.isVisible:
                textPalette.isVisible = True
                adsk.doEvents()

            doc = app.activeDocument
            products = doc.products

            # Make
            camWS = ui.workspaces.itemById('CAMEnvironment') 
            camWS.activate()
            cam = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))

            # Design creation
            designWS = ui.workspaces.itemById('FusionSolidEnvironment') 
            designWS.activate()
            design = adsk.fusion.Design.cast(products.itemByProductType("DesignProductType"))
            camWS.activate()

            libraryManager = adsk.cam.CAMManager.get().libraryManager
            templateLibrary = libraryManager.templateLibrary

            # The block below is the gist of this script.
            # Each method can be edited to fit the user's needs.
            (manufacturingModel, occs) = createManufacturingModel(cam)
            if manufacturingModel is None:
                return
            
            setup: adsk.cam.Setup = createAdditiveSetup(occs, cam, libraryManager)

            machineElements = setup.machine.elements
            machineDimsList: adsk.cam.AdditivePlatformMachineElement = machineElements.itemsByType(adsk.cam.AdditivePlatformMachineElement.staticTypeId())
            machineDims = machineDimsList[0]
            origin = machineDims.origin
            machineSize = machineDims.size

            maxPointX = - origin.x + machineSize.x
        
            createAdditiveArrange(setup, cam)

            ui.activeSelections.clear()
            ui.activeSelections.add(setup)

            app.activeViewport.fit()

            showMessage('Finished.')
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler that reacts to when the command is destroyed. This terminates the script if this has not happened before in an exception. 
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # When the command is done, terminate the script
            showMessage('Script is terminating.')
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            adsk.terminate()

# Event handler that reacts when the command definition is executed which
# results in the command being created and this event being fired.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)
        
            onExecute = MyCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

            onDestroy = MyCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            handlers.append(onDestroy)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    try:
        global app, ui

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = ui.commandDefinitions.itemById('MJFExampleScript')
        if not cmdDef:
            cmdDef = ui.commandDefinitions.addButtonDefinition('MJFExampleScript', 'MJF Example Script', 'Sample to demonstrate a workflow for MJF printers.')

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()
        
        # Keeps the script alive until it is terminated by the onDestroy event.
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Given an occurrence, this finds all child occurrences that contain either a
# B-Rep or Mesh body. It is recursive, so it will find all occurrences at all levels.
def getValidOccurrences(occurrence: adsk.fusion.Occurrence) -> list[adsk.fusion.Occurrence]:
    result = []
    for childOcc in occurrence.childOccurrences:
        if (childOcc.bRepBodies.count + childOcc.component.meshBodies.count  > 0):
            result.append(childOcc)

        result.extend(getValidOccurrences(childOcc))

    return result


def showMessage(message):
    app.log(message)

    # Give control back to Fusion, so it can update the UI.
    adsk.doEvents()
```

