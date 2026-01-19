# Manufacturing Workflow API Sample

## Description

Manufacturing Workflow API Sample

This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program.

## Code Samples

| Copy Code |
|----------:|

```python
import math, os, traceback
from enum import Enum
import adsk.fusion, adsk.core, adsk.cam

#################### Script Constants ####################
# We assume we are cutting Aluminum here...

# Milling tool library to get tools from
MILLING_TOOL_LIBRARY = 'Milling Tools (Metric)'

# Some material properties for feed and speed calculation
ALUMINUM_CUTTING_SPEED = 300  # mm/min
ALUMINUM_FEED_PER_TOOTH = 0.1 # mm/tooth

# Some tool preset names, known to exist for the selected tools
ALUMINUM_PRESET_ROUGHING = 'alu* rou*'
ALUMINUM_PRESET_FINISHING = 'Aluminum - Finishing'

#################### Useful Enumerators ####################
# Some tool types used in this script (enumerator)
class ToolType(Enum):
    BULL_NOSE_END_MILL = 'bull nose end mill'
    BALL_END_MILL = 'ball end mill'
    FACE_MILL = 'face mill'

# Setup work coordinate system (WCS) location (enumerator)
class SetupWCSPoint(Enum):
    TOP_CENTER = 'top center'
    TOP_XMIN_YMIN = 'top 1'
    TOP_XMAX_YMIN = 'top 2'
    TOP_XMIN_YMAX = 'top 3'
    TOP_XMAX_YMAX = 'top 4'
    TOP_SIDE_YMIN = 'top side 1'
    TOP_SIDE_XMAX = 'top side 2'
    TOP_SIDE_YMAX = 'top side 3'
    TOP_SIDE_XMIN = 'top side 4'
    CENTER = 'center'
    MIDDLE_XMIN_YMIN = 'middle 1'
    MIDDLE_XMAX_YMIN = 'middle 2'
    MIDDLE_XMIN_YMAX = 'middle 3'
    MIDDLE_XMAX_YMAX = 'middle 4'
    MIDDLE_SIDE_YMIN = 'middle side 1'
    MIDDLE_SIDE_XMAX = 'middle side 2'
    MIDDLE_SIDE_YMAX = 'middle side 3'
    MIDDLE_SIDE_XMIN = 'middle side 4'
    BOTTOM_CENTER = 'bottom center'
    BOTTOM_XMIN_YMIN = 'bottom 1'
    BOTTOM_XMAX_YMIN = 'bottom 2'
    BOTTOM_XMIN_YMAX = 'bottom 3'
    BOTTOM_XMAX_YMAX = 'bottom 4'
    BOTTOM_SIDE_YMIN = 'bottom side 1'
    BOTTOM_SIDE_XMAX = 'bottom side 2'
    BOTTOM_SIDE_YMAX = 'bottom side 3'
    BOTTOM_SIDE_XMIN = 'bottom side 4'

#################### Script Entry Point ####################
def run(context) -> None:
    ui = None
    try:

        #################### Initialisation #####################
        app = adsk.core.Application.get()
        ui: adsk.core.UserInterface  = app.userInterface
        
        # Create a new empty document
        doc: adsk.core.Document = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        # Get the design document used to create the sample part
        design: adsk.core.Product = app.activeProduct

        # Switch to manufacturing space
        camWS: adsk.core.Workspace = ui.workspaces.itemById('CAMEnvironment') 
        camWS.activate()

        # Get the CAM product
        products: adsk.core.Products = doc.products

        #################### Create Sample Part ####################

        part: adsk.fusion.BRepBody = createSamplePart(design)

        #################### Select Cutting Tools ####################

        # Get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager: adsk.cam.CAMLibraryManager = camManager.libraryManager
        toolLibraries: adsk.cam.ToolLibraries = libraryManager.toolLibraries

        url: adsk.core.URL = None
        libUrl = None
        useHardCodedUrl: bool = False
        if useHardCodedUrl:
            # We could use a library URl directly if we know its address ...
            libUrl = 'systemlibraryroot://Samples/Milling Tools (Metric).json'
            url = adsk.core.URL.create(libUrl)

        else:
            # ... or we can use the tool library objects
            # Fusion folder in the tool library
            fusionFolder: adsk.core.URL = toolLibraries.urlByLocation(adsk.cam.LibraryLocations.Fusion360LibraryLocation)
            fusionLibs: list[str] = getLibrariesURLs(toolLibraries, fusionFolder)
            
            # Search the required library url in the libraries
            for libUrl in fusionLibs:
                if MILLING_TOOL_LIBRARY in libUrl:
                    url = adsk.core.URL.create(libUrl)
                    break
        
        # Load the tool library
        toolLibrary: adsk.cam.ToolLibrary = toolLibraries.toolLibraryAtURL(url)

        # Create some variables to host the milling tools which will be used in the operations
        faceTool: adsk.cam.Tool = None
        adaptiveTool: adsk.cam.Tool = None
        finishingTool: adsk.cam.Tool = None

        # For the roughing operations, search for the face mill and the bull nose using a loop 
        for tool in toolLibrary:
            # Read the tool type
            toolType: adsk.cam.ToolType = tool.parameters.itemByName('tool_type').value.value 
            
            # Select the first face tool found
            if toolType == ToolType.FACE_MILL.value and not faceTool:
                faceTool = tool  
            
            # Search for the roughing tool
            elif toolType == ToolType.BULL_NOSE_END_MILL.value and not adaptiveTool:
                # Look for a bull nose end mill tool larger or equal to 12mm but less than 14mm
                diameter: float = tool.parameters.itemByName('tool_diameter').value.value
                if diameter >= 1.2 and diameter = stockY:
            input.parameters.itemByName('passAngle').expression = '0 deg' 
        else:
            input.parameters.itemByName('passAngle').expression = '90 deg'

        # Add the operation to the setup
        faceOp: adsk.cam.OperationBase = setup.operations.add(input)


        #################### Adaptive Operations ####################
        input = setup.operations.createInput('adaptive')
        input.tool = adaptiveTool
        input.displayName = 'Adaptive Roughing'
        input.parameters.itemByName('tolerance').expression = '0.1 mm' 
        input.parameters.itemByName('maximumStepdown').expression = '5 mm' 
        input.parameters.itemByName('fineStepdown').expression = '0.25 * maximumStepdown'
        input.parameters.itemByName('flatAreaMachining').expression = 'false'

        # Check if there is a tool preset related to aluminum roughing
        presets: adsk.cam.ToolPresets = adaptiveTool.presets.itemsByName(ALUMINUM_PRESET_ROUGHING)
        if len(presets) > 0:
            # Select the first preset found
            adaptivePreset: adsk.cam.ToolPreset = presets[0]
            input.toolPreset = adaptivePreset

        # Add the operation to the setup
        adaptiveOp: adsk.cam.OperationBase = setup.operations.add(input)


        #################### Finishing Tool Preset ####################
        # Select a tool preset from the finishing tool
        finishingPreset: adsk.cam.ToolPreset = None
        presets = finishingTool.presets.itemsByName(ALUMINUM_PRESET_FINISHING)
        if len(presets) > 0:
            # Use the first aluminum finishing preset found
            finishingPreset = presets[0]


        #################### Parallel Operations ####################
        input = setup.operations.createInput('parallel')
        input.tool = finishingTool
        input.displayName = 'Parallel Finishing'
        input.parameters.itemByName('tolerance').expression = '0.01 mm'
        input.parameters.itemByName('cuspHeightStepover').expression = '0.005 mm'
        input.parameters.itemByName('boundaryMode').expression = "'selection'"
        if finishingPreset:
            # Assign the finishing tool preset
            input.toolPreset = finishingPreset

        # Add the operation to the setup
        parallelOp: adsk.cam.OperationBase = setup.operations.add(input)

        # Lets use a contour for the sake of demonstration
        limitEdge: adsk.fusion.BRepEdge = None
        for e in part.edges:
            # This is the inner one: intersection of a plane and a sphere making up a circle
            if e.geometry.curveType == adsk.core.Curve3DTypes.Circle3DCurveType:
                limitEdge = e
                break

        if limitEdge:
            # Apply the limiting edge to the operation
            cadcontours2dParam: adsk.cam.CadContours2dParameterValue = parallelOp.parameters.itemByName('machiningBoundarySel').value
            chains: adsk.cam.CurveSelections = cadcontours2dParam.getCurveSelections()
            chain: adsk.cam.ChainSelection = chains.createNewChainSelection()
            chain.inputGeometry = [limitEdge]
            cadcontours2dParam.applyCurveSelections(chains)


        #################### Steep And Shallow Operations ####################
        # Create folder for finishing operations that require Machining Extension
        operationInput: adsk.cam.OperationInput = setup.operations.createInput('folder')
        operationInput.displayName = 'Machining Extension Required'
        folder: adsk.cam.CAMFolder = setup.operations.add(operationInput)

        # Create steep and shallow operation in the folder
        input = setup.operations.createInput('steep_and_shallow')
        input.tool = finishingTool
        input.displayName = 'Steep and Shallow Finishing'
        input.parameters.itemByName('tolerance').expression = '0.01 mm'
        input.parameters.itemByName('useAvoidFlats').expression = 'true'
        input.parameters.itemByName('cuspHeightStepdown').expression = '0.005 mm'
        input.parameters.itemByName('cuspHeightStepover').expression = 'cuspHeightStepdown'
        input.parameters.itemByName('spiral').expression = 'true'
        input.parameters.itemByName('shallowSpiral').expression = 'true'
        input.parameters.itemByName('offsetSmoothing').expression = 'true'

        # Assign the finishing tool preset
        if finishingPreset:
            input.toolPreset = finishingPreset

        # Add the operation to the folder
        steepAndShallowOp: adsk.cam.OperationBase = folder.operations.add(input)

        # Check if this toolpath is generatable as "steep_and_shallow" requires the manufacturing extension
        isSteepAndShallowGeneratable: bool = False
        for op in setup.operations.compatibleStrategies:
            if op.name == 'steep_and_shallow':
                if op.isGenerationAllowed:
                    # If isGenerationAllowed is False, the extension isn't active, preventing generation of the steep_and_shallow operation
                    isSteepAndShallowGeneratable = True
                break


        #################### Generate Operations ####################
        # Include the valid operations to generate
        operations = adsk.core.ObjectCollection.create()
        operations.add(faceOp)
        operations.add(adaptiveOp)
        operations.add(parallelOp)
        if isSteepAndShallowGeneratable:
            operations.add(steepAndShallowOp)

        # create progress bar
        progressDialog: adsk.core.ProgressDialog = ui.createProgressDialog()
        progressDialog.isCancelButtonShown = False
        progressDialog.show('Generating operations...', '%p%', 0, 100)
        adsk.doEvents() # Allow Fusion to update so the progressDialog shows up nicely

        # Generate the valid operations
        gtf: adsk.cam.GenerateToolpathFuture = cam.generateToolpath(operations)

        # Wait for the generation to be finished and update progress bar
        while not gtf.isGenerationCompleted:
            # Calculate progress and update progress bar
            total = gtf.numberOfOperations
            completed = gtf.numberOfCompleted
            progress = int(completed * 100 / total)
            progressDialog.progressValue = progress
            adsk.doEvents() # Allow Fusion to update so the screen doesn't freeze

        # Generation done
        progressDialog.progressValue = 100
        progressDialog.hide()
            

        #################### NC Program And Post-processing ####################
        # Get the post library from library manager
        postLibrary: adsk.cam.PostLibrary = libraryManager.postLibrary

        # Query post library to get postprocessor list
        postQuery: adsk.cam.PostConfigurationQuery = postLibrary.createQuery(adsk.cam.LibraryLocations.Fusion360LibraryLocation)
        postQuery.vendor = "Autodesk"
        postQuery.capability = adsk.cam.PostCapabilities.Milling
        postConfigs: list[adsk.cam.PostConfiguration] = postQuery.execute()

        # Find the "XYZ" post in the post library and import it to local library
        for config in postConfigs:
            if config.description == 'XYZ':
                url = adsk.core.URL.create("user://")
                importedURL: adsk.core.URL = postLibrary.importPostConfiguration(config, url, "NCProgramSamplePost.cps")

        # Get the imported local post config
        postConfig: adsk.cam.PostConfiguration = postLibrary.postConfigurationAtURL(importedURL)
       
        # Create NCProgramInput object
        ncInput: adsk.cam.NCProgramInput = cam.ncPrograms.createInput()
        ncInput.displayName = 'NC Program Sample'

        # Change some nc program parameters...
        ncParameters: adsk.cam.CAMParameters = ncInput.parameters
        ncParameters.itemByName('nc_program_filename').value.value = 'NCProgramSample'
        ncParameters.itemByName('nc_program_openInEditor').value.value = True

        # Set user desktop as output directory (Windows and Mac)
        # Make the path valid for Fusion by replacing \\ to / in the path
        desktopDirectory = os.path.expanduser("~/Desktop").replace('\\', '/') 
        ncParameters.itemByName('nc_program_output_folder').value.value = desktopDirectory
        
        # Select the operations to generate (we skip steep_and_shallow here)
        ncInput.operations = [faceOp, adaptiveOp, parallelOp]

        # Add a new ncprogram from the ncprogram input
        newProgram: adsk.cam.NCProgram = cam.ncPrograms.add(ncInput)

        # Set post processor
        newProgram.postConfiguration = postConfig

        # Change some post parameter
        postParameters: adsk.cam.CAMParameters = newProgram.postParameters

        # NcProgram parameters are passed as theyare to the postprocessor (they have no units)
        postParameters.itemByName('builtin_tolerance').value.value = 0.01 
        postParameters.itemByName('builtin_minimumChordLength').value.value = 0.33

        # Update/apply post parameters
        newProgram.updatePostParameters(postParameters)

        # Set post options, by default post process only valid operations containing toolpath data
        postOptions = adsk.cam.NCProgramPostProcessOptions.create()

        # Post-process
        newProgram.postProcess(postOptions)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


#################### Functions To Make Our Life Easier ####################

def getLibrariesURLs(libraries: adsk.cam.ToolLibraries, url: adsk.core.URL) -> list[str]:
    ''' Return the list of libraries' URLs for the specified libraries '''
    urls: list[str] = []
    libs: list[adsk.core.URL] = libraries.childAssetURLs(url)
    for lib in libs:
        urls.append(lib.toString())
    for folder in libraries.childFolderURLs(url):
        urls = urls + getLibrariesURLs(libraries, folder)
    return urls


def getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(toolLibrary: adsk.cam.ToolLibrary, tooltype: str, minDiameter: float, maxDiameter: float, minimumFluteLength: float = None) -> list[adsk.cam.Tool]:
    ''' Return a list of tools that satisfy the search '''
    query: adsk.cam.ToolQuery = toolLibrary.createQuery()
    # Set the search critera
    query.criteria.add('tool_type', adsk.core.ValueInput.createByString(tooltype))
    query.criteria.add('tool_diameter.min', adsk.core.ValueInput.createByReal(minDiameter))
    query.criteria.add('tool_diameter.max', adsk.core.ValueInput.createByReal(maxDiameter))
    if minimumFluteLength:
        query.criteria.add('tool_fluteLength.min', adsk.core.ValueInput.createByReal(minimumFluteLength))
    # Get query results
    results: list[adsk.cam.ToolQueryResult] = query.execute()
    # Get the tools from the query
    tools: list[adsk.cam.Tool] = []
    for result in results:
        # Results have a tool, url, toollibrary and the index of the tool in that library: we just return the tool here
        tools.append(result.tool)
    return tools


#################### CAD Creation ####################

def createSamplePart(design: adsk.fusion.Design) -> adsk.fusion.BRepBody:
    """ Creates the sample part for this script """
    # The sample part is a box containing a concave side generated by subtracting the intersection from a sphere.
    # The lower face of the box is at Z=0 and we position the sphere above but intersecting with the box upper face.
    # Fusion's default behaviour is now to ground the first component of an assembly to the parent. 
    # This can be overriden, see Preferences ->General ->Design ->Assemblies ->First component grounded to parent
    # However if we make the first component the box, we can move the sphere without changing anything

    box: adsk.fusion.BRepBody = createBox(design, 22, 15, 5) # 1st component occurrence
    sphere: adsk.fusion.BRepBody = createSphere(design, 7.5) # 2nd component occurrence

    # Get the root component
    rootComp: adsk.fusion.Component = design.rootComponent
    occs: adsk.fusion.Occurrences = rootComp.occurrences

    # Get the second Occurrence (sphere) as the first occurrence (box) may be grounded to the parent
    occ: adsk.fusion.Occurrence = occs.item(1)
    mat: adsk.core.Matrix3D = occ.transform
    
    # Matrix translation, moving the sphere up by 10 units along Z axis
    mat.translation = adsk.core.Vector3D.create(0, 0, 10)

    # Set transform
    occ.transform = mat

    # Snapshot - Determining the position is important!!!
    design.snapshots.add()

    # Cut the sphere/box intersection from the box to leave a concave face
    part: adsk.fusion.BRepBody = getBodyFromBooleanOperation(design, box, sphere)
    return part


def createBox(design: adsk.fusion.Design, sizeX: float, sizeY: float, sizeZ: float) -> adsk.fusion.BRepBody:
    ''' Creates a sample box'''
    component: adsk.fusion.Component = design.rootComponent
    # Create sketch
    sketches: adsk.fusion.Sketches = component.sketches
    sketch: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    lines: adsk.fusion.SketchLines = sketch.sketchCurves.sketchLines
    lines.addTwoPointRectangle(adsk.core.Point3D.create(-sizeX / 2, -sizeY / 2, 0), adsk.core.Point3D.create(sizeX / 2, sizeY / 2, 0))
    prof: adsk.fusion.Profile = sketch.profiles.item(0)
    extrudes: adsk.fusion.ExtrudeFeatures = component.features.extrudeFeatures
    distance = adsk.core.ValueInput.createByReal(sizeZ)
    ext: adsk.fusion.ExtrudeFeature = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
    return ext.bodies.item(0)


def createSphere(design: adsk.fusion.Design, radius: float) -> adsk.fusion.BRepBody:
    ''' Creates a sample sphere '''
    component: adsk.fusion.Component = design.rootComponent
    # Create a new sketch on the xy plane.
    sketches: adsk.fusion.Sketches = component.sketches
    xyPlane: adsk.fusion.ConstructionPlane = component.xYConstructionPlane
    sketch: adsk.fusion.Sketch = sketches.add(xyPlane)
    # Draw a circle.
    circles: adsk.fusion.SketchCircles = sketch.sketchCurves.sketchCircles
    circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
    # Draw a line to use as the axis of revolution.
    lines: adsk.fusion.SketchLines = sketch.sketchCurves.sketchLines
    axisLine: adsk.fusion.SketchLine = lines.addByTwoPoints(adsk.core.Point3D.create(-radius, 0, 0), adsk.core.Point3D.create(radius, 0, 0))
    # Get the profile defined by half of the circle.
    prof: adsk.fusion.Profile = sketch.profiles.item(0)
    # Create an revolution input for a revolution while specifying the profile and that a new component is to be created
    revolves: adsk.fusion.RevolveFeatures = component.features.revolveFeatures
    revInput: adsk.fusion.RevolveFeatureInput = revolves.createInput(prof, axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
    # Define that the extent is an angle of 2*pi to get a sphere
    angle = adsk.core.ValueInput.createByReal(2*math.pi)
    revInput.setAngleExtent(False, angle)
    # Create the extrusion.
    ext: adsk.fusion.RevolveFeature = revolves.add(revInput)
    return ext.bodies.item(0)


def getBodyFromBooleanOperation(design: adsk.fusion.Design, body1: adsk.fusion.BRepBody, body2: adsk.fusion.BRepBody) -> adsk.fusion.BRepBody:
    """ Creates a boolean operation between two bodies """
    model: adsk.fusion.Component = design.activeComponent
    features: adsk.fusion.Features = model.features
    # Create a collection and add our sphere
    bodyCollection = adsk.core.ObjectCollection.create()
    bodyCollection.add(body2)

    # Create a CombineFeatureInput using our box (body1), sphere (bodyCollection) specifying a 'cut' operation
    combineFeatures: adsk.fusion.CombineFeatures = features.combineFeatures
    combineFeatureInput: adsk.fusion.CombineFeatureInput = combineFeatures.createInput(body1, bodyCollection)
    combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combineFeatureInput.isKeepToolBodies = False
    combineFeatureInput.isNewComponent = False

    # Generate our combined feature
    returnValue: adsk.fusion.CombineFeature = combineFeatures.add(combineFeatureInput)
    part: adsk.fusion.BRepBody = returnValue.bodies[0]
    return part
```

