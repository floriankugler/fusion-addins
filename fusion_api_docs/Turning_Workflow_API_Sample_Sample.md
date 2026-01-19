# Turning Workflow API Sample

## Description

Turning Workflow API Sample

This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback
import time

# Address/urn of the sample project to load by the script
PROJECT_URN = 'urn:adsk.wipprod:fs.file:vf.484G2xc_Tx2ZOs6kSWmyXw?version=2' # CAM Samples -> API Samples -> Models -> Threaded_Mount

# local turning tool library to use
TURNING_TOOL_LIBRARY_NAME = 'Turning Tools (Metric)'


def run(context):
    ui = None
    try:

        #################### Initialisation #####################
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Load by URN a specific sample project to demonstrate a basic turning workflow.
        doc = loadProjectFromURN(PROJECT_URN)
        if not doc:
            return

        design = adsk.fusion.Design.cast(doc.products.itemByProductType("DesignProductType"))
        if not design:
            ui.messageBox('No active Fusion design found.', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
            return

        # Switch to manufacturing space
        camWS: adsk.core.Workspace = ui.workspaces.itemById('CAMEnvironment')
        camWS.activate()

        # Get the products (to get CAM product later...)
        products: adsk.core.Products = doc.products

        #################### Find tools in sample tool library ####################
        # Get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager: adsk.cam.CAMLibraryManager = camManager.libraryManager
        toolLibraries: adsk.cam.ToolLibraries = libraryManager.toolLibraries

        # Search for a specific turning tool library in local tool libraries
        toolLibrary: adsk.cam.ToolLibrary = None
        localLibLocationURL = toolLibraries.urlByLocation(adsk.cam.LibraryLocations.Fusion360LibraryLocation)
        localFolderURLs = toolLibraries.childAssetURLs(localLibLocationURL)
        for url in localFolderURLs:
            # search for tool library using its name name
            if url.leafName == TURNING_TOOL_LIBRARY_NAME:
                # Load tool library
                toolLibrary: adsk.cam.ToolLibrary = toolLibraries.toolLibraryAtURL(url)
                break

        # check tool library has been found
        if not toolLibrary:
            ui.messageBox(f'Failed to find tool library: "{TURNING_TOOL_LIBRARY_NAME}"', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
            return

        # Create some variables for the turning tools which will be used in the operations
        faceTool: adsk.cam.Tool = None
        roughingTool: adsk.cam.Tool = None

        # Searching the turning tool using a loop for the roughing operations
        for tool in toolLibrary:
            # Read the tool type
            toolType = tool.parameters.itemByName('tool_type').value.value
            hand = tool.parameters.itemByName('tool_hand').value.value
            shape = tool.parameters.itemByName('tool_insertType').value.value

            # Select the first face tool found
            if toolType == 'turning general' and hand == 'R' and shape == 'C' and not faceTool:
                tool.parameters.itemByName('tool_number').expression = '1'
                faceTool = tool

            # Search the roughing tool
            elif toolType == 'turning general' and hand == 'R' and shape == 'V' and not roughingTool:
                tool.parameters.itemByName('tool_number').expression = '2'
                roughingTool = tool

            # Exit when the 2 tools are found
            if faceTool and roughingTool:
                break

        #################### Create setup ####################
        cam: adsk.cam.CAM = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))
        setups: adsk.cam.Setups = cam.setups
        setupInput: adsk.cam.SetupInput = setups.createInput(adsk.cam.OperationTypes.TurningOperation)

        # Create a list for the models to add to the setup Input
        models = []

        # Identify the part or exit gracefully
        try:
            part: adsk.fusion.BRepBody = cam.designRootOccurrence.bRepBodies.item(0)
        except Exception as e:
            ui.messageBox('No part found in the current document, exiting sample script.', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
            return

        # Add the part to the model list
        models.append(part)
        # Pass the model list to the setup input
        setupInput.models = models
        # Create the setup
        setup: adsk.cam.Setup = setups.add(setupInput)
        # Change some properties of the setup
        setup.name = 'CAM Turning Basic Script Sample'
        setup.stockMode = adsk.cam.SetupStockModes.RelativeCylinderStock
        # Set offset mode
        setup.parameters.itemByName('job_stockOffsetMode').expression = "'simple'"
        # Set offset stock side
        setup.parameters.itemByName('job_stockOffsetSides').expression = '1 mm'
        # Set offset stock top
        setup.parameters.itemByName('job_stockOffsetTop').expression = '0.5 mm'
        # Set setup origin
        setup.parameters.itemByName('wcs_origin_boxPoint').value.value = 'top 1'

        #################### Face operation ####################
        # Create a face operation input
        faceInput: adsk.cam.OperationInput = setup.operations.createInput('turningFace')
        faceInput.tool = faceTool
        faceInput.displayName = 'Turning Facing Operation'
        faceInput.parameters.itemByName('tolerance').expression = '0.01 mm'
        faceInput.parameters.itemByName('stepover').expression = '0.75 * tool_diameter'
        faceInput.parameters.itemByName('direction').expression = "'outside to inside'"

        # Add the operation to the setup
        faceOp: adsk.cam.OperationBase = setup.operations.add(faceInput)

        #################### Adaptive operation ####################
        roughingInput = setup.operations.createInput('turningProfileRoughing')
        roughingInput.tool = roughingTool
        roughingInput.displayName = 'Turning Roughing Operation'
        roughingInput.parameters.itemByName('tolerance').expression = '0.1 mm'
        roughingInput.parameters.itemByName('depthOfCut').expression = '1.1 mm'

        # Add the operation to the setup
        roughingOp: adsk.cam.OperationBase = setup.operations.add(roughingInput)

        ##################### Generate operations ####################
        cam.generateToolpath(faceOp)
        genFuture: adsk.cam.GenerateToolpathFuture = cam.generateToolpath(roughingOp)
        adsk.doEvents()

        #################### ncProgram and post-processing ####################
        # Get the post library from library manager
        postLibrary: adsk.cam.PostLibrary = libraryManager.postLibrary

        # Query post library to get postprocessor list
        libraryLocation = adsk.cam.LibraryLocations.Fusion360LibraryLocation
        postQuery: adsk.cam.PostConfigurationQuery = postLibrary.createQuery(libraryLocation)
        postQuery.vendor = "Fanuc"
        postQuery.capability = adsk.cam.PostCapabilities.Turning
        postConfigs: list[adsk.cam.PostConfiguration] = postQuery.execute()

        # Find a post in the post library and import it to local library
        ncExtension = ''
        for config in postConfigs:
            if config.description == 'FANUC Turning':
                ncExtension = config.extension
                url = adsk.core.URL.create("user://")
                importedURL = postLibrary.importPostConfiguration(config, url, "NCProgramSampleTurnPost.cps")
                break

        # Get the imported local post config
        postConfig: adsk.cam.PostConfiguration = postLibrary.postConfigurationAtURL(importedURL)

        # Create NCProgramInput object
        ncInput: adsk.cam.NCProgramInput = cam.ncPrograms.createInput()
        ncInput.displayName = 'NC Program Sample'

        # Change some nc program parameters...
        ncFilename = 'NCProgramSample'
        ncParameters: adsk.cam.CAMParameters = ncInput.parameters
        ncParameters.itemByName('nc_program_filename').value.value = ncFilename
        ncParameters.itemByName('nc_program_openInEditor').value.value = True
        ncParameters.itemByName('nc_program_nc_extension').value.value = ncExtension

        # Set temp directory as output directory
        # Make the path valid for Fusion by replacing \\ to / in the path
        outputFolder = str(cam.temporaryFolder).replace('\\', '/')
        ncParameters.itemByName('nc_program_output_folder').value.value = outputFolder

        # Select the operations to generate
        ncInput.operations = [faceOp, roughingOp]

        # Add a new ncprogram from the ncprogram input
        newProgram: adsk.cam.NCProgram = cam.ncPrograms.add(ncInput)

        # Set post processor
        newProgram.postConfiguration = postConfig

        # Change some post parameters
        postParameters: adsk.cam.CAMParameters = newProgram.postParameters

        # NcProgram parameters are passed without units to the postprocessor
        postParameters.itemByName('builtin_tolerance').value.value = 0.01
        postParameters.itemByName('builtin_minimumChordLength').value.value = 0.33

        # Update/apply post parameters
        newProgram.updatePostParameters(postParameters)

        # Post-process
        # Set post options, by default post process only valid operations containing toolpath data
        postOptions = adsk.cam.NCProgramPostProcessOptions.create()

        # Ensure toolpaths are visible
        faceOp.isLightBulbOn = True
        roughingOp.isLightBulbOn = True

        # To avoid errors, post-process only when toolpath generation has completed
        while not genFuture.isGenerationCompleted:
            time.sleep(1)
        newProgram.postProcess(postOptions)

        # Advise where the NC file is located to indicate completion (adding a few Tabs '\t' so the file path is nicely printed on one line..)
        ui.messageBox(f'Setup, Operations and NCProgram created.\n\nThe results have been written to:\n{outputFolder}/{ncFilename}{ncExtension}\n\nPost processing is complete.  \t\t\t\t\t', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.InformationIconType)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()), 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)


def loadProjectFromURN(urn: str = None) -> adsk.core.Document:
    ''' Minimal self-contained function to load and return a document via URN or return None safely '''
    doc: adsk.core.Document = None
    app = adsk.core.Application.get()
    if urn:
        try:  # File not found causes an exception
            project: adsk.core.DataFile = app.data.findFileById(urn)
            if project:
                doc = app.documents.open(project, True)
            else:
                app.userInterface.messageBox(f'File not found for URN: {urn}!', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
        except Exception as e:
            if str(e)[0:38] == '3 : Design is located in another team.':
                # Although the document has been loaded, variable 'doc' may not be populated
                if not doc:
                    doc: adsk.core.Document = adsk.core.Application.get().activeDocument
            elif str(e)[0:20] == '3 : file not found':
                app.userInterface.messageBox(f'File not found for URN: {urn}!', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
            else:
                # Abandon for unhandled errors, displaying the error message.
                app.userInterface.messageBox(f'Failed:{str(e)}\n{traceback.format_exc()}', 'Fusion', adsk.core.MessageBoxButtonTypes.OKButtonType, adsk.core.MessageBoxIconTypes.CriticalIconType)
    return doc
```

