# Additive Manufacturing FFF API Sample

## Description

Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath.

To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input.

The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback, tempfile, time
from pathlib import Path

app = adsk.core.Application.get()
ui  = app.userInterface

def run(context):
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

        showMessage('=============================================')
        showMessage('Creating Manufacturing Model...')
        manufacturingModels = cam.manufacturingModels
        mmInput = manufacturingModels.createInput()
        mmInput.name = "My Manufacturing Model - FFF"
        manufacturingModel = manufacturingModels.add(mmInput)

        showMessage('Getting occurrences...')
        occs = getValidOccurrences(manufacturingModel.occurrence)
        if len(occs) == 0:
            ui.messageBox('No component has been added to the scene.')
            return 

        showMessage('Creating arrange operation...')
        setup = createAdditiveSetup(occs, cam)

        # Define and create the arrange operation.
        operationInput = setup.operations.createInput('additive_arrange')
        arrange = setup.operations.add(operationInput)

        parameter: adsk.cam.StringParameterValue = arrange.parameters.itemByName("arrange_arrangement_type").value
        parameter.value = 'Pack2D'

        # Specify the values to control the arrangement. All length units are centimeters.
        parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_sweetspot_option").value
        parameter.value = 'arrange_sweetspot_center'

        parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_platform_clearance").value
        parameter.value = 0

        parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_frame_width").value
        parameter.value = 0.5

        parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_ceiling_clearance").value
        parameter.value = 0.5              

        parameter: adsk.cam.FloatParameterValue = arrange.parameters.itemByName("arrange_object_spacing").value
        parameter.value = 1

        future = cam.generateToolpath(arrange)
        while (future.isGenerationCompleted == False):
            time.sleep(0.5)

        # Create the automatic orientation operations for each occurrence.
        for occ in occs:
            showMessage(f'Defining orientation for occurrence "{occ.name}" ...')
            operationInput = setup.operations.createInput('automatic_orientation')
            operationInput.isAutoCalculating = False
            orientationTarget = operationInput.parameters.itemByName('optimizeOrientationTarget')
            orientationTarget.value.value = [occ]
            operationInput.displayName = 'Automatic Orientation: ' + occ.name
            #global orientation
            orientation = setup.operations.add(operationInput)

            parameter: adsk.cam.FloatParameterValue = orientation.parameters.itemByName("optimizeOrientationSmallestRotation").value
            parameter.value = 180 #angle units are always degrees

            parameter: adsk.cam.BooleanParameterValue = orientation.parameters.itemByName("optimizeOrientationUsePreciseCalculation").value
            parameter.value = True #capitilize

            parameter: adsk.cam.FloatParameterValue = orientation.parameters.itemByName("optimizeOrientationCriticalAngle").value
            parameter.value = 45 #angle units are always degrees

            parameter: adsk.cam.FloatParameterValue = orientation.parameters.itemByName("optimizeOrientationDistanceToPlatform").value
            parameter.value = 0 #units are always cm

            parameter: adsk.cam.BooleanParameterValue = orientation.parameters.itemByName("optimizeOrientationMoveToCenter").value
            parameter.value = True #capitilize

            parameter: adsk.cam.FloatParameterValue = orientation.parameters.itemByName("optimizeOrientationFrameWidth").value
            parameter.value = 0.5 #units are always cm

            parameter: adsk.cam.FloatParameterValue = orientation.parameters.itemByName("optimizeOrientationCeilingClearance").value
            parameter.value = 0.5 #units are always cm

            parameter: adsk.cam.ChoiceParameterValue = orientation.parameters.itemByName("optimizeOrientationRankingSupportVolume").value
            parameter.value = '10' #take the number from dialog with its quotes

            parameter: adsk.cam.ChoiceParameterValue = orientation.parameters.itemByName("optimizeOrientationRankingSupportArea").value
            parameter.value = '0' #take the number from dialog with its quotes

            parameter: adsk.cam.ChoiceParameterValue = orientation.parameters.itemByName("optimizeOrientationRankingBoundingBoxVolume").value
            parameter.value = '2' #take the number from dialog with its quotes

            parameter: adsk.cam.ChoiceParameterValue = orientation.parameters.itemByName("optimizeOrientationRankingPartHeight").value
            parameter.value = '6' #take the number from dialog with its quotes

            parameter: adsk.cam.ChoiceParameterValue = orientation.parameters.itemByName("optimizeOrientationRankingCOGHeight").value
            parameter.value = '6' #take the number from dialog with its quotes

            showMessage('Generating orientation...')
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

        showMessage('Generating arrange...')
        future = cam.generateToolpath(arrange)
        while (future.isGenerationCompleted == False):
            time.sleep(0.5)

        showMessage('Generating supports...')
        supportInput = setup.operations.createInput('solid_volume_support')
        volumeSupport = setup.operations.add(supportInput)
        supportParam = volumeSupport.parameters.itemByName('supportTarget')
        supportParam.value.value = occs
        future = cam.generateToolpath(volumeSupport)
        while (future.isGenerationCompleted == False):
            time.sleep(0.5)

        if volumeSupport.hasError:
            volumeSupport.deleteMe()

        showMessage('Generating toolpath...')
        toolpath = None
        i = 0
        for i in range(setup.operations.count):
            op = setup.operations.item(i)
            if (op.strategy == 'additive_buildstyle'):
                toolpath = op
                break
        if (toolpath == None): 
            return

        future = cam.generateToolpath(toolpath)
        while (future.isGenerationCompleted == False):
           time.sleep(1.0)

        app.activeViewport.fit()

        res = ui.messageBox('Do you want to post the toolpath? Choosing "No" will display the simulation instead.', '', adsk.core.MessageBoxButtonTypes.YesNoButtonType, adsk.core.MessageBoxIconTypes.QuestionIconType)

        if res == adsk.core.DialogResults.DialogNo:
            # Start the toolpath simulation command.
            ui.commandDefinitions.itemById('IronAdditiveSimulation').execute()
        else:
            # Create the NC program
            ncprograms = cam.ncPrograms
            input = ncprograms.createInput()
            input.name = 'Prusa NCProgram'
            input.operations = [toolpath]
            ncprogram = ncprograms.add(input)

            params = ncprogram.parameters
            params.itemByName("nc_program_useMachineConfig").value.value = True
            params.itemByName("nc_program_openInEditor").value.value = False

            ncprogram.postConfiguration = getPostConfiguration()

            # Decide where to save the NC Program to
            # The default is to save it to disk
            fileDlg = ui.createFileDialog()
            fileDlg.title = 'Post Toolpath'
            fileDlg.filter = 'G-Code (*.gcode)'

            # Show file open dialog
            dlgResult = fileDlg.showSave()
            if dlgResult == adsk.core.DialogResults.DialogOK:
                path: Path = Path(fileDlg.filename)
                folderPath = str(path.parent.as_posix())
                fileName = path.name.replace('.gcode', '')
            else:
                ui.messageBox('Post cancelled, showing simulation instead.')
                ui.commandDefinitions.itemById('IronAdditiveSimulation').execute()
                return
            params.itemByName('nc_program_output_folder').expression = "\'"+folderPath+"\'"
            params.itemByName('nc_program_filename').expression =  "\'"+fileName+"\'"

            # Post the NC program
            postProcessOptions = adsk.cam.NCProgramPostProcessOptions.create()

            #----------- Post to Fusion Hub Sample ------------
            # Users can also choose to post the toolpath to FusionHub
            # In this case a new project and folder will be created in the user's active hub if they don't exist yet.

            #params.itemByName("nc_program_postToFusionTeam").value.value = True

            # This is the default, a dialog is raised to ask to save the project, cancelling the dialog will post the program, but without linking it to the project.
            #postProcessOptions.fusionHubExecutionBehavior = adsk.cam.FusionHubExecutionBehaviors.FusionHubExecutionBehavior_ExportWithRelationship
            # Same as above, except that cancelling the dialog will not post the program.
            #postProcessOptions.fusionHubExecutionBehavior = adsk.cam.FusionHubExecutionBehaviors.FusionHubExecutionBehavior_ForceExportWithRelationship
            # Saves the project if it has not been saved yet and links it to the posted program.
            #postProcessOptions.fusionHubExecutionBehavior = adsk.cam.FusionHubExecutionBehaviors.FusionHubExecutionBehavior_SilentForceExportWithRelationship
            # Only uploads the post, without linking the project.
            #postProcessOptions.fusionHubExecutionBehavior = adsk.cam.FusionHubExecutionBehaviors.FusionHubExecutionBehavior_SkipRelationship

            # Set the Fusion Hub folder to upload the post to
            #data = app.data
            #hub = data.activeHub
            #folder = createHubFolder(hub)
            #ncprogram.fusionHubFolder = folder

            #-------------------------------------------------
            ncprogram.postProcess(postProcessOptions)

        showMessage('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        adsk.terminate()


# Create an additive setup.
def createAdditiveSetup(models: list[adsk.fusion.Occurrence], cam: adsk.cam.CAM):
    setups = cam.setups
    input = setups.createInput(adsk.cam.OperationTypes.AdditiveOperation)
    input.models = models
    input.name = 'AdditiveSetup'

    camManager = adsk.cam.CAMManager.get()
    libraryManager = camManager.libraryManager
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
            if ps.name ==  "PLA (Direct Drive)": #print setting name from fusions library
                printSetting = ps
                break

        for machine in machines: #model name from fusions library -- Example: "Generic FFF Machine"
            if machine.model ==  "i3 MK3S+":
                machine = machine
                break
    input.machine = machine
    input.printSetting= printSetting
    setup = setups.add(input)
    return setup

def getPostConfiguration() -> adsk.cam.PostConfiguration:
    camManager = adsk.cam.CAMManager.get()
    libraryManager = camManager.libraryManager
    postConfigLibrary = libraryManager.postLibrary
    postConfigUrl = postConfigLibrary.urlByLocation(adsk.cam.LibraryLocations.Fusion360LibraryLocation)
    postConfigs = postConfigLibrary.childPostConfigurations(postConfigUrl)

    for config in postConfigs:
        if config.description == "Prusa":  # Example: "Prusa MK3S+"
            return config

    return None
def createHubFolder(hub:adsk.core.DataHub) -> adsk.core.DataFolder:
    # Create hub folder
    folder = None
    projectFound = None
    for project in hub.dataProjects:
        if project.name == "AdditiveFFFAutomationSamples":
            projectFound = project
            break

    # If the project is not found, create it
    if not projectFound:
        hub.dataProjects.add("AdditiveFFFAutomationSamples", "Post samples created by the Additive FFF Automation Samples script.")
    # And then create the folder we want to use as the post destination
    folder = projectFound.rootFolder.dataFolders.itemByName("AutomationSamples")
    if not folder:
        folder = projectFound.rootFolder.dataFolders.add("AutomationSamples")

    return folder

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

