# Hole and Pocket Recognition API Sample

## Description

This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets.

The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature.

RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations.

The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets.

This script works only if the Manufacturing Extension is active.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.fusion, adsk.core, adsk.cam, traceback
import math
from enum import Enum


#################### CONSTANTS & ENUMERATORS ####################
# Milling & drilling tool libraries to get tools from
MILLING_TOOL_LIBRARY_URL  = adsk.core.URL.create('systemlibraryroot://Samples/Milling Tools (Metric).json')
DRILLING_TOOL_LIBRARY_URL = adsk.core.URL.create('systemlibraryroot://Samples/Hole Making Tools (Metric).json')

# Colors
POCKET_WALL_FACES_COLOR   = adsk.core.Color.create(0, 255, 255, 255)
POCKET_BOTTOM_FACES_COLOR = adsk.core.Color.create(0, 145, 230, 255)
HOLE_SIMPLE_COLOR         = adsk.core.Color.create(130, 225, 10, 255)
HOLE_COUNTERBORE_COLOR    = adsk.core.Color.create(180, 120, 255, 255)

# Tool types used in this script (enumerator)
class ToolType(Enum):
    BULL_NOSE_END_MILL = 'bull nose end mill'
    DRILL              = 'drill'
    FLAT_END_MILL      = 'flat end mill'
    SPOT_DRILL         = 'spot drill'

# Pocket search vector: only look for pockets from top view: visible and machinable from Z+
POCKET_SEARCH_VECTOR = adsk.core.Vector3D.create(0, 0, -1)


#################### ENTRY POINT #####################
def run(context) -> None:
    try:       
        app = adsk.core.Application.get()
        ui: adsk.core.UserInterface = app.userInterface

        # Create a new empty document
        doc: adsk.core.Document = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        # Switch to manufacturing space
        camWS: adsk.core.Workspace = ui.workspaces.itemById('CAMEnvironment') 
        camWS.activate()

        # Get the CAM product
        products: adsk.core.Products = doc.products
        cam: adsk.cam.CAM = products.itemByProductType("CAMProductType")

        # Get the CAD product
        design: adsk.fusion.Design = products.itemByProductType('DesignProductType')

        # Get the root component of the active design as we will need to create sketches later on...
        rootComponent: adsk.fusion.Component = design.rootComponent
        sketches:adsk.fusion.Sketches = rootComponent.sketches

        #################### CREATE SAMPLE PART ####################

        body: adsk.fusion.BRepBody = createSampleBody(rootComponent)

        # Refresh screen and fit model to view
        app.activeViewport.refresh()
        app.activeViewport.fit()
        adsk.doEvents()

        #################### TOOL LIBRARIES ####################

        # Get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager: adsk.cam.CAMLibraryManager = camManager.libraryManager
        toolLibraries: adsk.cam.ToolLibraries = libraryManager.toolLibraries
        
        # Load tool libraries
        millingToolLibrary: adsk.cam.ToolLibrary = toolLibraries.toolLibraryAtURL(MILLING_TOOL_LIBRARY_URL)
        drillingToolLibrary: adsk.cam.ToolLibrary = toolLibraries.toolLibraryAtURL(DRILLING_TOOL_LIBRARY_URL)

        ####################### HOLE & POCKETS RECOGNITION - SAMPLE SCRIPT MAIN LOGIC STARTS #######################

        # Create setups
        holeRecognitionSetup: adsk.cam.Setup = createSetup('Holes (using "RecognizedHoleGroup")', body) 
        pocketRecognitionSetup: adsk.cam.Setup = createSetup('Pockets (using "RecognizedPocket")', body)
        pocketSelectionSetup: adsk.cam.Setup = createSetup('Pockets (using "PocketRecognitionSelection")', body)

        # Get body parent component
        pocketComponent: adsk.fusion.Component = body.parentComponent

        # Get a tool to machine the pockets
        tools: list[adsk.cam.Tool] = getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(millingToolLibrary, ToolType.FLAT_END_MILL.value, 1, 1, 2)
        roughingTool: adsk.cam.Tool = tools[0] # Use the first tool found

        ########## MAKE POCKETS USING POCKET RECOGNITION API ##########

        # Recognize pockets
        pockets: adsk.cam.RecognizedPockets = adsk.cam.RecognizedPocket.recognizePockets(body, POCKET_SEARCH_VECTOR)

        # Variable used to capture operations created
        op: adsk.cam.Operation = None

        # List of operations created, used to highlight them once created
        ops: list[adsk.cam.Operation] = []

        # Get boundary key points to find bottom faces (if any) and create roughing operation
        for pocket in pockets:
            # Check if the pocket is circular (if it's basically a simple hole) since we will deal with those using drilling
            if isCircularPocket(pocket):
                continue

            # Pocket boundaries
            boundaries: list[adsk.core.Curve3DPath] = pocket.boundaries

            # Get pocket boundary key points (used later on to find and color faces)
            points: list[adsk.core.Point3D] = []
            for boundary in boundaries:
                boundaryPoints: list[adsk.core.Point3D] = getBoundaryKeyPoints(boundary)
                points.extend(boundaryPoints)

            # Create pocket operations
            if pocket.isThrough:
                # THROUGH POCKETS: Searching the side faces for coloring. Bottom faces are missing so we will draw sketch to define pocket bottom boundary.
                
                # Search the wall faces as breps using the points of the boundary
                _, pocketWallFaces = getPocketBottomAndWallFaces(pocket)

                # Color the pocket walls
                colorFaces(design, pocketWallFaces, 'pocketWallFacesColor', POCKET_WALL_FACES_COLOR)

                # Create a sketch on XY plane since there is no bottom face to use here
                sketch: adsk.fusion.Sketch = sketches.add(rootComponent.xYConstructionPlane)
                sketch.name = 'Through pocket sketch'
                drawSketchCurves(sketch, boundary)

                # Create an operation using that sketch
                op = createClosedThroughPocketOperation(pocketRecognitionSetup, 'Closed through pocket', sketch, pocket, roughingTool)
                ops.append(op)
                
            else:
                # BLIND POCKETS: Search the pocket bottom face to use in the operation and side faces for coloring.

                # Get the bottom and wall face breps of a pocket
                pocketBottomFaces, pocketWallFaces = getPocketBottomAndWallFaces(pocket)

                # Color the pocket bottom faces
                colorFaces(design, pocketBottomFaces, 'pocketBottomFaces', POCKET_BOTTOM_FACES_COLOR)

                # Color the pocket walls
                colorFaces(design, pocketWallFaces, 'pocketWallFacesColor', POCKET_WALL_FACES_COLOR)

                # Define the pocket name
                name = 'Closed blind pocket' if pocket.isClosed else 'Open blind pocket'

                op = createBlindPocketOperation(pocketRecognitionSetup, name, pocketBottomFaces, pocket, roughingTool)
                ops.append(op)

            # ask Fusion to refresh the screen
            app.activeViewport.refresh()


        ########## MAKE POCKETS USING POCKET RECOGNITION SELECTION (FROM UI) ##########

        # Create basic roughing operations
        # The distinction between the pockets is done by filtering the pocket heights, within the functions below...
        op = createClosedThroughPocketSelectionOperation(pocketSelectionSetup, 'Closed through pocket (PocketSelection)', roughingTool)
        ops.append(op)

        op = createClosedBlindPocketSelectionOperation(pocketSelectionSetup, 'Closed blind pocket (PocketSelection)', roughingTool)
        ops.append(op)
        

        ########## MAKE HOLES USING HOLE GROUP RECOGNITION API ##########

        # Hole group recognition using "RecognizedHoleGroup()" is grouping holes of the same type  
        # You could also use "RecognizedHole()": this will give you all holes but ungrouped...
        recognizedHolesInput = adsk.cam.RecognizedHolesInput.create()
        holeGroups: adsk.cam.RecognizedHoleGroups = adsk.cam.RecognizedHoleGroup.recognizeHoleGroupsWithInput([body], recognizedHolesInput)
        
        # Loop through the hole groups found
        for holeGroup in holeGroups:
            
            # Analyze the first hole from the group to understand their geometry (hole from a group are all the same)
            holeToCheck: adsk.cam.RecognizedHole = holeGroup.item(0)

            # Check the number of segments and the geometry that makes the hole to identify the hole type
            if holeToCheck.segmentCount == 1:
                firstSegment: adsk.cam.RecognizedHoleSegment = holeToCheck.segment(0)
                if firstSegment.holeSegmentType == adsk.cam.HoleSegmentType.HoleSegmentTypeCylinder:
                    # This is a simple hole made of one cylinder so let's drill that hole group
                    
                    # Color the faces
                    for hole in holeGroup:
                        simpleHoleFaces :list[adsk.fusion.BRepFace] = []
                        simpleHoleFaces.extend(hole.segment(0).faces)
                        colorFaces(design, simpleHoleFaces, 'simpleHoleColor', HOLE_SIMPLE_COLOR)

                    # Tool selection
                    drillDiameter: float = firstSegment.bottomDiameter # Check hole diameter to select the right drill
                    drillDepth: float = firstSegment.height + 0.5 # Check the hole length to make sure the drill is long enough... and add a clearance of 5mm
                    drillTools: list[adsk.cam.Tool] = getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(drillingToolLibrary, ToolType.DRILL.value, drillDiameter, drillDiameter, drillDepth)
                    drillTool: adsk.cam.Tool = drillTools[0] # Select the first tool found
                    
                    # Create the operation
                    op = createSimpleDrillOperation('Simple drill', holeRecognitionSetup, drillTool, holeGroup)
                    ops.append(op)

            elif holeToCheck.segmentCount == 4:
                # A hole with 4 segments might be a counterbore through model with a top chamfer... so let's check the geometry...
                firstSegment: adsk.cam.RecognizedHoleSegment = holeToCheck.segment(0)
                secondSegment: adsk.cam.RecognizedHoleSegment = holeToCheck.segment(1)
                thirdSegment: adsk.cam.RecognizedHoleSegment = holeToCheck.segment(2)
                fourthSegment: adsk.cam.RecognizedHoleSegment = holeToCheck.segment(3)

                if firstSegment.holeSegmentType == adsk.cam.HoleSegmentType.HoleSegmentTypeCone:
                    if secondSegment.holeSegmentType == adsk.cam.HoleSegmentType.HoleSegmentTypeCylinder:
                        if thirdSegment.holeSegmentType == adsk.cam.HoleSegmentType.HoleSegmentTypeFlat:
                            if fourthSegment.holeSegmentType == adsk.cam.HoleSegmentType.HoleSegmentTypeCylinder:
                                # A hole made by a cone, a cylinder, a flat and finally a cylinder is our definition of a counterbore through model with a top chamfer, in this example
                                # We will ignore other types of hole made by 4 segments here if any...

                                # Color the faces
                                for hole in holeGroup:
                                    couterboreHoleFaces :list[adsk.fusion.BRepFace] = []
                                    couterboreHoleFaces.extend(hole.segment(0).faces)
                                    couterboreHoleFaces.extend(hole.segment(1).faces)
                                    couterboreHoleFaces.extend(hole.segment(2).faces)
                                    couterboreHoleFaces.extend(hole.segment(3).faces)
                                    colorFaces(design, couterboreHoleFaces, 'counterboreHoleColor', HOLE_COUNTERBORE_COLOR)

                                # Tool selection
                                drillDiameter:float = fourthSegment.bottomDiameter # Check hole diameter to select the right drill
                                # Check the hole length to make sure the drill is long enough... and add a clearance of 5mm
                                drillDepth:float = firstSegment.height + secondSegment.height + fourthSegment.height + 0.5 # No need to use the third segment height as it's a flat face
                                drillTools: list[adsk.cam.Tool] = getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(drillingToolLibrary, ToolType.DRILL.value, drillDiameter, drillDiameter, drillDepth)
                                drillTool:adsk.cam.Tool = drillTools[0] # Select the first tool found
                                
                                # Create the drill operation
                                op = createCounterboreDrillOperation('Counterbore drill', holeRecognitionSetup, drillTool, holeGroup)
                                ops.append(op)

                                # Check the counterbopre diameter to select the right flat end mill
                                # We will drill the hole first meaning we don't need to take this into account...
                                # Select a flat end mill for the counterbore
                                minCounterboreToolDiameter: float = secondSegment.bottomDiameter - fourthSegment.bottomDiameter
                                maxCounterboreToolDiameter: float = secondSegment.bottomDiameter * 0.75
                                counterboreToolMinFluteLength: float =  firstSegment.height + secondSegment.height + 0.5 # Adding 5mm clearance
                                counterboreTools: list[adsk.cam.Tool] = getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(millingToolLibrary, ToolType.FLAT_END_MILL.value, minCounterboreToolDiameter, maxCounterboreToolDiameter, counterboreToolMinFluteLength)
                                counterboreTool: adsk.cam.Tool = counterboreTools[0] # Select the first tool found
                                
                                # Counterbore
                                op = createCounterboreMillOperation('Counterbore mill', holeRecognitionSetup, counterboreTool, holeGroup)
                                ops.append(op)

                                # Select tools
                                # Pick a spot drill tool for the top chamfer (we will roll over the chamfer so no need for a very large tool)
                                minChamferToolDiameter:float = 1
                                maxChamferToolDiameter:float = 1.4
                                chamferTools: list[adsk.cam.Tool] = getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(drillingToolLibrary, ToolType.SPOT_DRILL.value, minChamferToolDiameter, maxChamferToolDiameter)
                                chamferTool: adsk.cam.Tool = chamferTools[0] # Pick first tool found
                                # Create chamfer operation
                                op = createCounterboreChamferOperation('Counterbore chamfer', holeRecognitionSetup, chamferTool, holeGroup)
                                ops.append(op)

            # ask Fusion to refresh the screen
            app.activeViewport.refresh()

        # Compute all tool paths
        cam.generateAllToolpaths(True)

        # Highligt the operations created
        for op in ops:
            ui.activeSelections.add(op)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

####################### SAMPLE SCRIPT MAIN LOGIC ENDS #######################
#############################################################################


####################### TOOLS #######################

def getToolsFromLibraryByTypeDiameterRangeAndMinFluteLength(toolLibrary: adsk.cam.ToolLibrary, tooltype: str, minDiameter: float, maxDiameter: float, minimumFluteLength: float = None) -> list[adsk.cam.Tool]:
    ''' Return a list of tools that fits the search '''
    # Define the search critera
    query: adsk.cam.ToolQuery = toolLibrary.createQuery()
    query.criteria.add('tool_type', adsk.core.ValueInput.createByString(tooltype))
    query.criteria.add('tool_diameter.min', adsk.core.ValueInput.createByReal(minDiameter))
    query.criteria.add('tool_diameter.max', adsk.core.ValueInput.createByReal(maxDiameter))
    if minimumFluteLength:
        query.criteria.add('tool_fluteLength.min', adsk.core.ValueInput.createByReal(minimumFluteLength))

    # Get the query results
    results: list[adsk.cam.ToolQueryResult] = query.execute()

    # Get the tools from the query
    tools: list[adsk.cam.Tool] = []
    for result in results:
        # A valid result has a tool, url, toolLibrary and the index of the tool in that library: we just return the tool here
        tools.append(result.tool)
    return tools


####################### SETUPS #######################

def createSetup(name: str, body: adsk.fusion.BRepBody) -> adsk.cam.Setup: 
    ''' Create a setup '''
    app = adsk.core.Application.get()
    doc: adsk.core.Document = app.activeDocument
    products: adsk.core.Products = doc.products
    cam = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))
    setups: adsk.cam.Setups = cam.setups

    # Create setup input and set the parameters
    input: adsk.cam.SetupInput = setups.createInput(adsk.cam.OperationTypes.MillingOperation)
    input.models = [body] 
    input.name = name  
    input.stockMode = adsk.cam.SetupStockModes.RelativeBoxStock
    input.parameters.itemByName('job_stockOffsetMode').expression = "'keep'"

    # Create the setup
    setup: adsk.cam.Setup = setups.add(input) 
    return setup


####################### POCKETS (USING API) #######################

def createClosedThroughPocketOperation(setup: adsk.cam.Setup, name: str, sketch: adsk.fusion.Sketch, pocket: adsk.cam.RecognizedPocket, tool: adsk.cam.Tool) -> adsk.cam.Operation:
    ''' Produce the toolpath for the closed through pocket using API '''
    input: adsk.cam.OperationInput = setup.operations.createInput('adaptive2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('doMultipleDepths').expression = 'true'
    pocketHeightIncludingBottomOffsetInMM: float = round((pocket.depth  * 10) + 2, 3)  # Convert cm to mm and add 2 mm from bottomHeight_offset
    input.parameters.itemByName('maximumStepdown').expression = str(pocketHeightIncludingBottomOffsetInMM / 2) + ' mm' # Divide total height by 2 to get 2 passes
    input.parameters.itemByName('topHeight_mode').expression = "'from contour'"
    input.parameters.itemByName('topHeight_offset').expression = str(pocket.depth * 10) + ' mm'
    input.parameters.itemByName('bottomHeight_offset').expression = str(-2) + 'mm' # Set bottom to be 2 mm below pocket bottom

    # Apply the sketch boundary to the operation input
    pocketSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('pockets').value
    chains: adsk.cam.CurveSelections = pocketSelection.getCurveSelections()
    chain: adsk.cam.SketchSelection = chains.createNewSketchSelection()
    chain.inputGeometry = [sketch]
    chain.loopType = adsk.cam.LoopTypes.OnlyOutsideLoops
    chain.sideType = adsk.cam.SideTypes.AlwaysInsideSideType
    pocketSelection.applyCurveSelections(chains)

    # Add to the setup
    op: adsk.cam.OperationBase = setup.operations.add(input)   
    return op


def createBlindPocketOperation(setup: adsk.cam.Setup, name: str, pocketBottomFaces: list[adsk.fusion.BRepFace], pocket: adsk.cam.RecognizedPocket, tool: adsk.cam.Tool) -> adsk.cam.Operation:
    ''' Produce the toolpath for the closed blind pocket using API '''
    input: adsk.cam.OperationInput = setup.operations.createInput('adaptive2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('doMultipleDepths').expression = 'true'
    input.parameters.itemByName('maximumStepdown').expression = str(round(pocket.depth / 2, 3) * 10) + ' mm' # Divide total height by 2 to get 2 passes
    input.parameters.itemByName('topHeight_mode').expression = "'from contour'"
    input.parameters.itemByName('topHeight_offset').expression = str(pocket.depth * 10) + ' mm'

    # Apply the limits edge to the operation input
    pocketSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('pockets').value
    chains: adsk.cam.CurveSelections = pocketSelection.getCurveSelections()
    chain: adsk.cam.PocketSelection = chains.createNewPocketSelection()
    chain.inputGeometry = pocketBottomFaces
    pocketSelection.applyCurveSelections(chains) 

    # Add to the setup
    op: adsk.cam.OperationBase = setup.operations.add(input)
    return op


####################### POCKETS (USING UI) #######################

def createClosedThroughPocketSelectionOperation(setup: adsk.cam.Setup, name: str, tool: adsk.cam.Tool) -> adsk.cam.Operation:
    ''' Produce the toolpath for the closed through pocket using UI '''
    input: adsk.cam.OperationInput = setup.operations.createInput('adaptive2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('doMultipleDepths').expression = 'true'
    input.parameters.itemByName('maximumStepdown').expression = '12 mm' # Divide the pocket height by 2 to ensure 2 steps
    input.parameters.itemByName('bottomHeight_offset').expression = str(-2) + ' mm' # Bottom height = 2 mm below pocket bottom


    # Apply the sketch boundary to the operation input
    pocketSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('pockets').value
    chains: adsk.cam.CurveSelections = pocketSelection.getCurveSelections()
    chain: adsk.cam.PocketRecognitionSelection = chains.createNewPocketRecognitionSelection()
    chain.maximumPocketDepth = 2.5 # (cm) Define some pocket recognition settings to filter pockets by height (measured from UI)
    chain.minimumPocketDepth = 1.5 # (cm)
    pocketSelection.applyCurveSelections(chains)

    # Add to the setup
    op: adsk.cam.Operation = setup.operations.add(input)
    return op


def createClosedBlindPocketSelectionOperation(setup: adsk.cam.Setup, name: str, tool: adsk.cam.Tool) -> adsk.cam.Operation:
    ''' Produce the toolpath for the closed blind pocket using UI '''
    input: adsk.cam.OperationInput = setup.operations.createInput('adaptive2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('doMultipleDepths').expression = 'true'
    input.parameters.itemByName('maximumStepdown').expression = '6 mm'

    # Apply the sketch boundary to the operation input
    pocketSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('pockets').value
    chains: adsk.cam.CurveSelections = pocketSelection.getCurveSelections()
    chain: adsk.cam.PocketRecognitionSelection = chains.createNewPocketRecognitionSelection()
    chain.maximumPocketDepth = 1.5 # (cm) Define some pocket recognition settings to filter pockets by height (measured from UI)
    chain.minimumPocketDepth = 0   # (cm)
    pocketSelection.applyCurveSelections(chains)

    # Add to the setup
    op: adsk.cam.OperationBase = setup.operations.add(input)
    return op


####################### POCKET HELPER FUNCTION #######################

def isCircularPocket(pocket: adsk.cam.RecognizedPocket) -> bool:
    ''' Returns true if this is a circular pocket (= a hole) made of boundaries with circular segments only '''
    isCircleFound: bool = False
    boundaries: list[adsk.core.Curve3DPath] = pocket.boundaries
    for i in range(len(boundaries)):
        boundary: adsk.core.Curve3DPath = boundaries[i]
        for j in range(boundary.count):
            segment: adsk.core.Curve3D = boundary.item(j)
            if segment.classType() == adsk.core.Circle3D.classType(): 
                isCircleFound = True
            else:
                return False
            
    return isCircleFound


def getBoundaryKeyPoints(boundary: list[adsk.core.Curve3DPath]) -> list[adsk.core.Point3D]:
    ''' Get some key points on the pocket boundary '''
    points: list[adsk.core.Point3D] = []
    for segment in boundary:
        # Cast to get the actual segment type (casting returns None if the wrong object is passed)
        line3D = adsk.core.Line3D.cast(segment)
        arc3D  = adsk.core.Arc3D.cast(segment)

        if line3D:
            points.append(line3D.startPoint)
            points.append(line3D.endPoint)
        elif arc3D:
            points.append(arc3D.startPoint)
            points.append(arc3D.endPoint)
        else:
            classType = segment.classType()
            raise Exception('Unsupported pocket curve type for this sample script: ' + classType)
    
    return points


def getPocketBottomAndWallFaces(pocket: adsk.cam.RecognizedPocket) -> tuple[list[adsk.fusion.BRepFace], list[adsk.fusion.BRepFace]]:
    ''' Get the pocket bottom and wall faces '''
    pocketBottomFaces: list[adsk.fusion.BRepFace] = []
    pocketWallFaces: list[adsk.fusion.BRepFace] = []

    for face in pocket.faces:
        _, n = face.evaluator.getNormalAtPoint(face.pointOnFace)
        # check if the face normal vector is parallel to the search vector
        # using "isParallelTo()" instead of "isEqualTo()" since the face normal is opposite to the pocket search vector
        if n.isParallelTo(POCKET_SEARCH_VECTOR):
            pocketBottomFaces.append(face)
        else:
            pocketWallFaces.append(face)
        
    return pocketBottomFaces, pocketWallFaces


####################### DRILLING #######################

def createSimpleDrillOperation(name: str, setup: adsk.cam.Setup, tool: adsk.cam.Tool, holeGroup: adsk.cam.RecognizedHoleGroup) -> adsk.cam.Operation:
    ''' Create simple drilling operation '''
    input: adsk.cam.OperationInput = setup.operations.createInput('drill')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('drillTipThroughBottom').expression = 'true'
    input.parameters.itemByName('breakThroughDepth').expression = '2 mm'

    # Select the hole faces to drill
    faces: list[adsk.fusion.BRepFace] = []
    for i in range(holeGroup.count):
        hole: adsk.cam.RecognizedHole = holeGroup.item(i)
        firstSegment: adsk.cam.RecognizedHoleSegment = hole.segment(0)
        faces.extend(firstSegment.faces)
    holeSelection: adsk.cam.CadObjectParameterValue = input.parameters.itemByName('holeFaces').value
    holeSelection.value = faces

    # Add to the setup
    op: adsk.cam.Operation = setup.operations.add(input)
    return op


def createCounterboreDrillOperation(name: str, setup: adsk.cam.Setup, tool: adsk.cam.Tool, holeGroup: adsk.cam.RecognizedHoleGroup) -> adsk.cam.Operation:
    ''' Create drilling operation for the counterbore hole '''
    input: adsk.cam.OperationInput = setup.operations.createInput('drill')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('drillTipThroughBottom').expression = 'true'
    input.parameters.itemByName('breakThroughDepth').expression = '2 mm'

    # Select the hole faces to drill
    faces: list[adsk.fusion.BRepFace] = []
    for i in range(holeGroup.count):
        hole: adsk.cam.RecognizedHole = holeGroup.item(i)
        firstSegment: adsk.cam.RecognizedHoleSegment = hole.segment(0)
        secondSegment: adsk.cam.RecognizedHoleSegment = hole.segment(1)
        fourthSegment: adsk.cam.RecognizedHoleSegment = hole.segment(3)
        faces.extend(firstSegment.faces)
        faces.extend(secondSegment.faces)
        faces.extend(fourthSegment.faces)
    holeSelection: adsk.cam.CadObjectParameterValue = input.parameters.itemByName('holeFaces').value
    holeSelection.value = faces

    # Add to the setup
    op: adsk.cam.Operation = setup.operations.add(input)
    return op


def createCounterboreMillOperation(name: str, setup: adsk.cam.Setup, tool: adsk.cam.Tool, holeGroup: adsk.cam.RecognizedHoleGroup) -> adsk.cam.Operation:
    ''' Create milling operation for the counterbore part of the hole '''
    input: adsk.cam.OperationInput = setup.operations.createInput('contour2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('doLeadIn').expression = 'false'
    input.parameters.itemByName('doRamp').expression = 'true'
    input.parameters.itemByName('rampAngle').expression = '2 deg'
    input.parameters.itemByName('exit_verticalRadius').expression = '0 mm'
    input.parameters.itemByName('exit_radius').expression = '0 mm'

    # Select the counterbore bottom edge to mill
    edges: list[adsk.fusion.BRepEdge] = []
    for i in range(holeGroup.count):
        hole: adsk.cam.RecognizedHole = holeGroup.item(i)
        secondSegment: adsk.cam.RecognizedHoleSegment = hole.segment(1) # Counterbore segment
        edge: adsk.fusion.BRepEdge = getHoleSegmentBottomEdge(secondSegment)
        edges.append(edge)
    holeSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('contours').value
    chains: adsk.cam.CurveSelections = holeSelection.getCurveSelections()

    # Each edge is a separate chain selection since they are owned by different holes
    for edge in edges:
        chain: adsk.cam.ChainSelection = chains.createNewChainSelection()
        chain.isReverted = True
        chain.inputGeometry = [edge]
    holeSelection.applyCurveSelections(chains) 

    # Add to the setup
    op: adsk.cam.Operation = setup.operations.add(input)
    return op


def createCounterboreChamferOperation(name: str, setup: adsk.cam.Setup, tool: adsk.cam.Tool, holeGroup: adsk.cam.RecognizedHoleGroup) -> adsk.cam.Operation:
    ''' Create an operation for the top chamfer of the counterbore '''
    input: adsk.cam.OperationInput = setup.operations.createInput('chamfer2d')
    input.displayName = name
    input.tool = tool
    input.parameters.itemByName('chamferClearance').expression = '0 mm'
    input.parameters.itemByName('entry_distance').expression = '5 mm'
    input.parameters.itemByName('chamferTipOffset').expression = '1 mm'

    # Select the counterbore chamfer's bottom edge to mill
    edges: list[adsk.fusion.BRepEdge] = []
    for i in range(holeGroup.count):
        hole: adsk.cam.RecognizedHole = holeGroup.item(i)
        firstSegment: adsk.cam.RecognizedHoleSegment = hole.segment(0) # Chamfer segment
        edge: adsk.fusion.BRepEdge = getHoleSegmentBottomEdge(firstSegment)
        edges.append(edge)
    holeSelection: adsk.cam.CadContours2dParameterValue = input.parameters.itemByName('contours').value
    chains: adsk.cam.CurveSelections = holeSelection.getCurveSelections()

    for edge in edges:
        # Each edge is a separate chain selection since they are owned by different holes
        chain: adsk.cam.ChainSelection = chains.createNewChainSelection()
        chain.isReverted = True
        chain.inputGeometry = [edge] 
    holeSelection.applyCurveSelections(chains) 

    # Add to the setup
    op: adsk.cam.Operation = setup.operations.add(input)
    return op


def getHoleSegmentBottomEdge(segment: adsk.cam.RecognizedHoleSegment) -> adsk.fusion.BRepEdge:
    ''' Get the bottom edge of a given hole segment (assuming the hole is algned on Z+) '''
    # We assume:
    #  - the segment is made by one face
    #  - the hole is aligned with Z+ (bounding box checking)
    if len(segment.faces) != 1:
        raise Exception('A hole segment with a single face is expected!')

    face = adsk.fusion.BRepFace.cast(segment.faces[0]) 
    faceEdges: adsk.fusion.BRepEdges = face.edges
    edge: adsk.fusion.BRepEdge = None
    if len(faceEdges) != 2:
        raise Exception('A hole segment with a single face made of 2 edges is expected!')
    if faceEdges[0].boundingBox.maxPoint.z  None:
    ''' Create a sketch from given pocket boundary or island '''
    for segment in boundary:
        # Cast to get the actual segment type (casting returns None if the wrong object is passed)
        line3D = adsk.core.Line3D.cast(segment)
        arc3D = adsk.core.Arc3D.cast(segment)
        circle3D = adsk.core.Circle3D.cast(segment)

        if line3D:
            startPoint: adsk.core.Point3D = line3D.startPoint
            endPoint: adsk.core.Point3D = line3D.endPoint
            sketchLine(sketch, startPoint, endPoint)
        elif arc3D:
            startPoint: adsk.core.Point3D = arc3D.startPoint
            centerPoint: adsk.core.Point3D = arc3D.center
            sweepAngle: float = arc3D.endAngle
            normal: adsk.core.Vector3D = arc3D.normal
            sketchTwoPointArc(sketch, centerPoint, startPoint, sweepAngle, normal)           
        elif circle3D:
            centerPoint: adsk.core.Point3D = circle3D.center
            radius: float = circle3D.radius
            sketchCircles(sketch, centerPoint, radius)
        else:
            classType = segment.classType()
            raise Exception('Unsupported pocket curve type for this sample script: ' + classType)

    mergeCoincidentPoints(sketch)


def mergeCoincidentPoints(sketch: adsk.fusion.Sketch) -> None:
    ''' Merge sketchpoints that are coincident. '''
    endPoints: list[adsk.fusion.SketchPoint] = []

    # Get the end points of all lines and arcs.
    for skLine in sketch.sketchCurves.sketchLines:
        endPoints.append(skLine.startSketchPoint)
        endPoints.append(skLine.endSketchPoint)

    for skArc in sketch.sketchCurves.sketchArcs:
        endPoints.append(skArc.startSketchPoint)
        endPoints.append(skArc.endSketchPoint)

    # Check if the points are at the same location and add a constraint.
    for i in range(len(endPoints)):
        point1: adsk.fusion.SketchPoint = endPoints[i]
        if not point1 is None:
            for j in range(i+ 1, len(endPoints)):
                point2: adsk.fusion.SketchPoint = endPoints[j]
                if not point2 is None:
                    if point1.geometry.isEqualTo(point2.geometry):
                        point1.merge(point2)
                        endPoints[i] = None
                        endPoints[j] = None


def sketchCircles(sketch: adsk.fusion.Sketch, centerPoint: adsk.core.Point3D, radius: float) -> adsk.fusion.SketchCircle:
    ''' Create a circle based on the points  '''
    circles: adsk.fusion.SketchCircles = sketch.sketchCurves.sketchCircles
    circle: adsk.fusion.SketchCircle = circles.addByCenterRadius(centerPoint, radius)
    return circle


def sketchTwoPointArc(sketch: adsk.fusion.Sketch, centerPoint: adsk.core.Point3D, startPoint: adsk.core.Point3D, sweepAngle: float, normal: adsk.core.Vector3D) -> adsk.fusion.SketchArc:
    ''' Sketch a arc based on center, radius and sweepangle '''
    arcs: adsk.fusion.SketchArcs = sketch.sketchCurves.sketchArcs
    arc: adsk.fusion.SketchArc = arcs.addByCenterStartSweep(centerPoint, startPoint, sweepAngle)
    arcNormal: adsk.core.Vector3D = arc.geometry.normal
    # Check whether the arc is drawn in the right direction
    if not arcNormal.z - normal.z  adsk.fusion.SketchLine:
    ''' Sketch a straight line based on the starting and ending points '''
    lines: adsk.fusion.SketchLines = sketch.sketchCurves.sketchLines
    line: adsk.fusion.SketchLine = lines.addByTwoPoints(startPoint, endPoint)
    return line


####################### COLORING #######################

def colorFaces(design: adsk.fusion.Design, faces: list[adsk.fusion.BRepFace], colorName: str, color: adsk.core.Color) -> None:
    ''' Color given BRepFaces '''
    app = adsk.core.Application.get()

    # Look for the color
    fusionMaterials: adsk.core.MaterialLibrary = app.materialLibraries.itemById('BA5EE55E-9982-449B-9D66-9F036540E140')
    newColor: adsk.core.Appearance = design.appearances.itemByName(colorName)
    if not newColor:
        # Get the existing Red appearance.            
        redColor: adsk.core.Appearance = fusionMaterials.appearances.itemById('Prism-093')
        # Copy it to the design, giving it a new name.
        newColor: adsk.core.Appearance = design.appearances.addByCopy(redColor, colorName)                    
        # Change the color of the default appearance to the provided one.
        theColor: adsk.core.ColorProperty = newColor.appearanceProperties.itemById('opaque_albedo')
        theColor.value = color

    # Color given faces
    for face in faces:
        face.appearance = newColor

    # ask Fusion to update graphics
    app.activeViewport.refresh()


####################### CREATE SAMPLE PART #######################

def createSampleBody(component: adsk.fusion.Component) -> adsk.fusion.BRepBody:
    ''' Create a sample part for the script '''
    app = adsk.core.Application.get()

    # Get reference to the sketchs
    sketches: adsk.fusion.Sketches = component.sketches

    # Get the extrude features Collection for the component
    extrudes: adsk.fusion.ExtrudeFeatures = component.features.extrudeFeatures
    chamfers: adsk.fusion.ChamferFeatures = component.features.chamferFeatures
    
    # Create a cuiboid
    rectangle: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    rectangle.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(22.0, 15.0, 0))
    blockExtrude: adsk.fusion.ExtrudeFeature = createExtrudeFeature(extrudes, rectangle, 2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Create a simple hole
    holeOne: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    circleOne: list[adsk.core.Circle3D] = [adsk.core.Circle3D.createByCenter(adsk.core.Point3D.create(3, 11.5, 2), adsk.core.Vector3D.create(0, 0, 1), 0.5)]
    drawSketchCurves(holeOne, circleOne)
    createExtrudeFeature(extrudes, holeOne, -2, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Create another simple hole
    holeTwo: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    circleTwo: list[adsk.core.Circle3D] = [adsk.core.Circle3D.createByCenter(adsk.core.Point3D.create(5, 11.5, 2), adsk.core.Vector3D.create(0, 0, 1), 0.5)]
    drawSketchCurves(holeTwo, circleTwo)
    createExtrudeFeature(extrudes, holeTwo, -2, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Create six counterbore holes
    sk: adsk.fusion.Sketch = sketches.add(blockExtrude.endFaces[0])
    skPoints = adsk.core.ObjectCollection.create()
    for i in range(1, 3):
        for j in range(1, 4):
            pstn = adsk.core.Point3D.create(3 * j, 3 * i, 0)
            skPoint: adsk.fusion.SketchPoint = sk.sketchPoints.add(pstn)
            skPoints.add(skPoint)

    holes: adsk.fusion.HoleFeatures = component.features.holeFeatures
    counterBoreDiam = adsk.core.ValueInput.createByReal(2)
    counterBoreDepth = adsk.core.ValueInput.createByReal(1)
    holeDiam = adsk.core.ValueInput.createByReal(1)
    holeInput: adsk.fusion.HoleFeatureInput = holes.createCounterboreInput(holeDiam, counterBoreDiam, counterBoreDepth)
    holeInput.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
    holeInput.setPositionBySketchPoints(skPoints)
    holeFeature: adsk.fusion.HoleFeature = holes.add(holeInput)

    # Find the top edges of the holes to add a chamfer.
    topFace: adsk.fusion.BRepFace = blockExtrude.endFaces[0]
    chamferEdges = adsk.core.ObjectCollection.create()
    for cylinderFace in holeFeature.faces:
        if isinstance(cylinderFace.geometry, adsk.core.Cylinder):
            commonEdge: adsk.fusion.BRepEdge = findCommonEdge(cylinderFace, topFace)
            if commonEdge:
                chamferEdges.add(commonEdge)

    # Create the chamfer
    chamferInput: adsk.fusion.ChamferFeatureInput = chamfers.createInput2()
    offset = adsk.core.ValueInput.createByReal(0.3)
    chamferInput.chamferEdgeSets.addEqualDistanceChamferEdgeSet(chamferEdges, offset, False)
    chamfers.add(chamferInput)

    # Create a closed pocket
    pocketOne: adsk.fusion.Sketch =  sketches.add(component.xYConstructionPlane)
    geometries: list[adsk.core.Curve3D] = []
    geometries.append(adsk.core.Line3D.create(adsk.core.Point3D.create(12, 1.5, 2),adsk.core.Point3D.create(13, 1.5, 2)))
    geometries.append(adsk.core.Line3D.create(adsk.core.Point3D.create(14, 2.5, 2),adsk.core.Point3D.create(14, 4.5, 2)))
    geometries.append(adsk.core.Line3D.create(adsk.core.Point3D.create(13, 5.5, 2),adsk.core.Point3D.create(12, 5.5, 2)))
    geometries.append(adsk.core.Line3D.create(adsk.core.Point3D.create(11, 4.5, 2),adsk.core.Point3D.create(11, 2.5, 2)))
    geometries.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(12, 2.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(-1, 0, 0), 1, 0, math.pi / 2))
    geometries.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(13, 2.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(0, -1, 0), 1, 0, math.pi / 2))
    geometries.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(13, 4.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(1, 0, 0), 1, 0, math.pi / 2))
    geometries.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(12, 4.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(0, 1, 0), 1, 0, math.pi / 2))
    drawSketchCurves(pocketOne, geometries)
    createExtrudeFeature(extrudes, pocketOne, -1, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Create a open pocket
    pocketTwo: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    pocketTwoOutline: list[adsk.core.Curve3D] = []
    pocketTwoOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(12, 7.5, 2),adsk.core.Point3D.create(18, 7.5, 2)))
    pocketTwoOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(19, 8.5, 2),adsk.core.Point3D.create(19, 11.5, 2)))
    pocketTwoOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(18, 12.5, 2),adsk.core.Point3D.create(12, 12.5, 2)))
    pocketTwoOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(11, 11.5, 2),adsk.core.Point3D.create(11, 8.5, 2)))
    pocketTwoOutline.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(12, 8.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(-1,0,0), 1, 0, math.pi / 2))
    pocketTwoOutline.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(18, 8.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(0,-1,0), 1, 0, math.pi / 2))
    pocketTwoOutline.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(18, 11.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(1,0,0), 1, 0, math.pi / 2))
    pocketTwoOutline.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(12, 11.5, 2), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Vector3D.create(0,1,0), 1, 0, math.pi / 2))
    drawSketchCurves(pocketTwo, pocketTwoOutline)
    createExtrudeFeature(extrudes, pocketTwo, -2, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Create a pocket on the side
    pocketThree: adsk.fusion.Sketch =  sketches.add(component.xYConstructionPlane)
    pocketThreeOutline: list[adsk.core.Curve3D] = []
    pocketThreeOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(18, 0, 2),adsk.core.Point3D.create(22, 0, 2)))
    pocketThreeOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(22, 0, 2),adsk.core.Point3D.create(22, 4.5, 2)))
    pocketThreeOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(22, 4.5, 2),adsk.core.Point3D.create(19, 4.5, 2)))
    pocketThreeOutline.append(adsk.core.Line3D.create(adsk.core.Point3D.create(18, 3.5, 2),adsk.core.Point3D.create(18, 0, 2)))
    pocketThreeOutline.append(adsk.core.Arc3D.createByCenter(adsk.core.Point3D.create(19, 3.5, 2), adsk.core.Vector3D.create(0,0,1), adsk.core.Vector3D.create(0, 1, 0), 1, 0, math.pi / 2))
    drawSketchCurves(pocketThree, pocketThreeOutline)
    createExtrudeFeature(extrudes, pocketThree, -1.5, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Return the created body
    part: adsk.fusion.BRepBody = component.bRepBodies.item(0)
    return part


def createExtrudeFeature(extrudeFeatures: adsk.fusion.ExtrudeFeatures, sketch:adsk.fusion.Sketch, height: float, operation: adsk.fusion.FeatureOperations) -> adsk.fusion.ChamferFeature:
    ''' Create an extrude feature '''
    # Get the profile defined by the circle
    shape: adsk.fusion.Profile = sketch.profiles.item(0)

    # Define that the extent is a distance extent of 1 cm
    distance = adsk.core.ValueInput.createByReal(height)

    # Create the extrusion
    extrudeFeature: adsk.fusion.ExtrudeFeature = extrudeFeatures.addSimple(shape, distance, operation)
    return extrudeFeature


# Find the edge that connects to the input faces.
def findCommonEdge(face1: adsk.fusion.BRepFace, face2: adsk.fusion.BRepFace) -> adsk.fusion.BRepEdge:
    # Checks to see if any of the edges of face1 connect to face2.
    edge: adsk.fusion.BRepEdge = None
    for edge in face1.edges:
        for face in edge.faces:
            if face == face2:
                return edge
            
    return None
```

