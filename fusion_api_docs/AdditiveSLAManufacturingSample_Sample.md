# Additive Manufacturing SLA API Sample

## Description

Demonstrates how to automate the creation of an additive SLA manufacturing setup.

To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input.

The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component.

The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback, tempfile, time

app = adsk.core.Application.get()
ui  = app.userInterface

# Global set of event handlers to keep them referenced for the duration of the command
handlers = []

def getTemplateFromLibrary(templateLibrary: adsk.cam.CAMTemplateLibrary, libLocation: adsk.cam.LibraryLocations, folderName: str, templateNameSubstring: str):
    libraryURL = templateLibrary.urlByLocation(libLocation)
    
    templates = None
    if folderName == "":
        templates = templateLibrary.childTemplates(libraryURL)
    else:
        childFolders = templateLibrary.childFolderURLs(libraryURL)
        pickedFolderURL = None
        for folderURL in childFolders:
            if folderURL.leafName.lower() == folderName.lower():
                pickedFolderURL = folderURL
                break
        templates = templateLibrary.childTemplates(pickedFolderURL)

    pickedTemplate = None
    for template in templates:
        lowerCaseName: str = template.name.lower()
        if lowerCaseName.find(templateNameSubstring.lower()) != -1:
            pickedTemplate = template
            break
    return pickedTemplate

def createManufacturingModel(cam: adsk.cam.CAM):
    showMessage('=============================================')
    showMessage('Creating Manufacturing Model...')
    manufacturingModels = cam.manufacturingModels
    mmInput = manufacturingModels.createInput()
    mmInput.name = "My Manufacturing Model - SLA"
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
            if ps.name ==  "Prusa SL1S SPEED - Prusament Resin Tough - 0.05mm Normal": #print setting name from fusions library
                printSetting = ps
                break

        for machine in machines: #model name from fusions library -- Example: "Generic SLA Machine"
            if machine.model ==  "SL1S SPEED":
                machine = machine
                break
    input.machine = machine
    input.printSetting= printSetting
    setup = setups.add(input)
    return setup

def createOrientations(templateLibrary: adsk.cam.CAMTemplateLibrary, occs: list[adsk.fusion.Occurrence], setup: adsk.cam.Setup, cam: adsk.cam.CAM):
    # the second parameter can be any of the following:
    # - adsk.cam.LibraryLocations.Fusion360LibraryLocation
    # - adsk.cam.LibraryLocations.LocalLibraryLocation
    # - adsk.cam.LibraryLocations.CloudLibraryLocation 
    # the third parameter is the folder name in the library
    # using the empty string for the root folder will search the templates in the top level folder instead
    # the fourth parameter is the substring to search for in the template name
    orientationTemplate = getTemplateFromLibrary(templateLibrary, adsk.cam.LibraryLocations.Fusion360LibraryLocation, "orientations", "SLA - Automatic Orientation")
    if orientationTemplate is None:
        showMessage('No orientation template found.')
        return
    orientationTemplateInput: adsk.cam.CreateFromCAMTemplateInput = adsk.cam.CreateFromCAMTemplateInput.create()
    orientationTemplateInput.camTemplate = orientationTemplate

    # Create the automatic orientation operations for each occurrence.
    for occ in occs:
        showMessage(f'Generating Automatic Orientation for "{occ.name}" ...')
        orientations =  setup.createFromCAMTemplate2(orientationTemplateInput)
        orientation = orientations[0]
        orientation.name = 'Automatic Orientation: ' + occ.name

        orientationTarget = orientation.parameters.itemByName('optimizeOrientationTarget')
        orientationTarget.value.value = [occ]

        future = cam.generateToolpath(orientation)
        while (future.isGenerationCompleted == False):
            time.sleep(0.5)

        generatedResults = orientation.generatedDataCollection
        castPref = None
        firstResult = None
        primary = generatedResults.itemByIdentifier(adsk.cam.GeneratedDataType.OptimizedOrientationGeneratedDataType)

        if isinstance(primary, adsk.cam.OptimizedOrientationResults):
            castPref: adsk.cam.OptimizedOrientationResults = primary
            firstResult = castPref.item(0)

        castPref.currentOrientationResult = firstResult

def createAdditiveArrange(setup: adsk.cam.Setup, cam: adsk.cam.CAM):
    # Define and create the arrange operation.
    showMessage('Generating Additive Arrange...')
    operationInput = setup.operations.createInput('additive_arrange')
    arrange = setup.operations.add(operationInput)

    parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_arrangement_type").value
    parameter.value = 'Pack2D'

    # Specify the values to control the arrangement. All length units are centimeters.
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_sweetspot_option").value
    parameter.value = 'arrange_sweetspot_center'
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_platform_clearance").value
    parameter.value = 0.7
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_frame_width").value
    parameter.value = 0.5
    
    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_ceiling_clearance").value
    parameter.value = 0.5              

    parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_object_spacing").value
    parameter.value = 1

    future = cam.generateToolpath(arrange)
    while (future.isGenerationCompleted == False):
        time.sleep(0.5)

def createSupports(templateLibrary: adsk.cam.CAMTemplateLibrary, occs: list[adsk.fusion.Occurrence], setup: adsk.cam.Setup, cam: adsk.cam.CAM):
    showMessage('Generating Supports...')
    # the second parameter can be any of the following:
    # - adsk.cam.LibraryLocations.Fusion360LibraryLocation
    # - adsk.cam.LibraryLocations.LocalLibraryLocation
    # - adsk.cam.LibraryLocations.CloudLibraryLocation 
    # the third parameter is the folder name in the library
    # using the empty string for the root folder will search the templates in the top level folder instead
    # the fourth parameter is the substring to search for in the template name    
    pickedTemplate = getTemplateFromLibrary(templateLibrary, adsk.cam.LibraryLocations.Fusion360LibraryLocation, "supports", "SLA - Braced Bar Support")
    if pickedTemplate is None:
        showMessage('No support template found.')
        return
    supportTemplateInput = adsk.cam.CreateFromCAMTemplateInput.create()
    supportTemplateInput.camTemplate = pickedTemplate
    
    supports = setup.createFromCAMTemplate2(supportTemplateInput)
    if len(supports) == 0:
        showMessage('No supports created.')
        return
    
    for support in supports:
        parameterName = 'supportTarget'
        if (support.parameters.itemByName('supportTarget') == None):
            parameterName = 'supportTargetModel'
        supportParam = support.parameters.itemByName(parameterName)
        supportParam.value.value = occs
        support.isLightBulbOn = True
    

    future = cam.generateToolpath(supports[0])
    while (future.isGenerationCompleted == False):
        time.sleep(0.5)

    for support in supports:
        if support.hasError:
            showMessage(f'Support generation failed for object {support.name}: {support.errorMessage}')
            support.deleteMe()
    
    for i in range(setup.children.count):
        op = setup.children.item(i)
        if (op and op.strategy == "additive_support_folder"):
            op.isLightBulbOn = True
            break

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
        
            createOrientations(templateLibrary, occs, setup, cam)
            createAdditiveArrange(setup, cam)

            curatedOccs = []
            for occ in occs:
                if occ.preciseBoundingBox.minPoint.x  list[adsk.fusion.Occurrence]:
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

