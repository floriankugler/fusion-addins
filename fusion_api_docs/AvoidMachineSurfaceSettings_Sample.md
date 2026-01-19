# Avoid Machine Surface Settings API Sample

## Description

This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality.

The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid.

The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback

dupName = 'Avoid/Machine using API'
information = f"""
This sample script demonstrates Machine/Avoid/Gouge/Fixture functionality. 
Move this dialog to one side and notice the following about the default operation:

    The existing operation machines the top face (yellow) and within the slot and hole.
    The supporting blocks (red) and the fixture plate (purple) are needlessly machined.
    We want it to avoid machining the top face, the fixture and within the slot and hole.
    Cap surfaces are provided for the slot and hole (colored green when set to visible).
    The mounting blocks are designated sacrificial so we can machine vertical walls fully.

To achieve this, we duplicate the first operation and assign labels to surface groups.
Both radial and axial “stock-to-leave” values can also be applied.

Acknowledge this dialog and select the operation named "{dupName}" 
to see the new improved tool path.
"""

#################### Global Variables ####################
_app = adsk.core.Application.get()
_ui = _app.userInterface
_machineAvoidGroups: adsk.cam.MachineAvoidGroups = None
_cam: adsk.cam.CAM = None
_design: adsk.fusion.Design = None

# This URN should point to the project beneath the CAM Samples folder.
PROJECT_URN = 'urn:adsk.wipprod:fs.file:vf.rxjQ68iyTN2ui31aDQULDw?version=1' # MachineAvoidAfter.

# Map the strategies to surface colors for a clearer indication.
modes = ['Avoid', 'Machine', 'Gouge', 'Fixture']
modeColor: dict[str, adsk.core.Color] = {
    modes[adsk.cam.MachiningMode.Avoid_MachiningMode]:      adsk.core.Color.create(255, 255, 113, 30), # Yellow
    modes[adsk.cam.MachiningMode.Machine_MachiningMode]:    adsk.core.Color.create(104, 255,   0, 30), # Green
    modes[adsk.cam.MachiningMode.Gouge_MachiningMode]:      adsk.core.Color.create(204,  51,  51, 30), # Red
    modes[adsk.cam.MachiningMode.Fixture_MachiningMode]:    adsk.core.Color.create(180, 120, 255, 30), # Purple
}

# The main script function.
def run(context):
    global _cam, _design, _machineAvoidGroups
    try:

        # Load by URN a specific sample project that demonstrates machine/avoid/ignore/gouge.
        doc = loadProjectFromURN(PROJECT_URN)
        if doc is None: 
            return
        products = doc.products

        # Switch to the manufacturing workspace (CAM environment).
        camWS = _app.userInterface.workspaces.itemById('CAMEnvironment') 
        camWS.activate()
        _cam = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))

        # Get the CAD product.
        _design = products.itemByProductType('DesignProductType')

        setups = _cam.setups

        # Ensure the document contains a Setup and then use the 1st setup in the document.
        if setups.count > 0:
            setup = setups.item(0) 
        else:
            userMessageBox('This script requires that there is a Setup in the Fusion Document', True)
            return

        operations = setup.operations

        # Remove all but the first operation as this script is not using the intended sample model
        for opNum in range(1,operations.count):
            operations.item(opNum).deleteMe()

        # Duplicate the first operation in the setup.
        if operations.count > 0:
            opOriginal = operations.item(0)
        else:
            userMessageBox('This script requires that there is an existing operation in the Setup.', True)
            return
        
        opOriginal.isLightBulbOn = True            
        opOriginal.duplicate()
        opDuplicate = operations.item(1)
        opDuplicate.name = dupName
        _app.log(f'The toolpath "{opOriginal.name}" has been duplicated and then renamed as "{opDuplicate.name}"')

        # Get the "checkSurfaceSelectionSets" parameter from the operation, which is a CadFaceGroups cad object.
        surfaceGroupsParam: adsk.cam.CadMachineAvoidGroupsParameterValue = opDuplicate.parameters.itemByName('checkSurfaceSelectionSets').value

        # Get the MachineAvoidGroups object from the CadFaceGroups cad object. This object manages the list of mutually exclusive groups.
        _machineAvoidGroups = surfaceGroupsParam.getMachineAvoidGroups() 

        # Create a Machine group comprising the two green coloured caps over the curved surface. Not visible by default.
        if not createMachineAvoidGroup('Selection Set3', adsk.cam.MachiningMode.Machine_MachiningMode, 0.2, 0.1):
            return

        # Create an Avoid group comprising the yellow coloured uppermost horizontal face.
        if not createMachineAvoidGroup('Selection Set1', adsk.cam.MachiningMode.Avoid_MachiningMode, 0.05, 0.02):
            return

        # Create a Fixture group comprising the purple coloured base block.
        if not createMachineAvoidGroup('fixture_base', adsk.cam.MachiningMode.Fixture_MachiningMode, 5.0, 0.6):
            return

        # Create an Ignore/Gouge group comprising the 1st red colored sacrificial support block.
        if not createMachineAvoidGroup('sacrificial_block1', adsk.cam.MachiningMode.Gouge_MachiningMode):
            return

        # Create an Ignore/Gouge group comprising the 2nd red colored sacrificial support block.
        if not createMachineAvoidGroup('sacrificial_block2', adsk.cam.MachiningMode.Gouge_MachiningMode):
            return

        # Add the groups back to the parameter.
        surfaceGroupsParam.applyMachineAvoidGroups(_machineAvoidGroups)

        # Explain what has happened and how to see the result
        userMessageBox(information)

        # Generate the operation.
        _cam.generateToolpath(opDuplicate)

        # Display the new toolpath - this is ineffective - user needs to select the path themselves.
        opOriginal.isLightBulbOn = False
        opDuplicate.isLightBulbOn = True
        opDuplicate.isToolpathVisible = True

        # Give control back to Fusion so it can update the graphics.
        adsk.doEvents()
        return

    except Exception as e:
        userMessageBox(f'Failed:: {e}\n{traceback.format_exc()}', True)

#################### Functions ####################

def createMachineAvoidGroup(name: str, mode: adsk.cam.MachiningMode, axialOffset: float = None, radialOffset: float = None):
    '''Create a Machine/Avoid group of the specified mode and name using the stated offsets if applicable'''
    machineAvoidGroup: adsk.cam.MachineAvoidDirectSelection = _machineAvoidGroups.createNewMachineAvoidDirectSelectionGroup()
    machineAvoidGroup.machineMode = mode

    # Gouge groups require no offsets to be specified.
    if mode != adsk.cam.MachiningMode.Machine_MachiningMode:
        if radialOffset is not None:
            machineAvoidGroup.radialOffset = radialOffset
        if axialOffset is not None:
            machineAvoidGroup.axialOffset = axialOffset

    if mode == adsk.cam.MachiningMode.Machine_MachiningMode or mode == adsk.cam.MachiningMode.Avoid_MachiningMode:
        faceSelSet = _design.selectionSets.itemByName(name)
        if faceSelSet:
            machineAvoidGroup.inputGeometry = faceSelSet.entities
        else:
            userMessageBox(f'The Selection Set "{name}" does not exist in the current Fusion document', True)
            return False
    else:
        # Add the face/body/component to the exclusiveGroup selection.
        bodySelect = _cam.designRootOccurrence.bRepBodies.itemByName(name)       
        if bodySelect:
            machineAvoidGroup.inputGeometry = getFacesAll(bodySelect)
        else:
            userMessageBox(f'The Body "{name}" does not exist in the current Fusion document', True)
            return False
    colorFaces(machineAvoidGroup.inputGeometry, mode)
    return True


def getFacesAll(body: adsk.fusion.BRepBody):
    ''' Adds all the faces in the selected body to a list '''
    allFaces: list[adsk.fusion.BRepFace] = []                               
    for face in body.faces:
         allFaces.append(face)                 
    return allFaces


def userMessageBox(messageText: str, isWarning: bool = False):
    ''' Keep messageBox calls informative but succinct'''
    iconType = adsk.core.MessageBoxIconTypes.WarningIconType if isWarning else adsk.core.MessageBoxIconTypes.InformationIconType
    _ui.messageBox(messageText, 'Fusion\t\t\t\t\t\t', adsk.core.MessageBoxButtonTypes.OKButtonType, iconType) # Title tabs widen messageBox.
    

def colorFaces(faces: list[adsk.fusion.BRepFace], mode: adsk.cam.MachiningMode):
    ''' Color specified BRepFaces '''
    modeName = modes[mode]
    for face in faces:
        # Check if "colorAppearance" already exists, if not, create it.
        appearances = _design.appearances
        colorAppearance = appearances.itemByName(modeName)

        if not colorAppearance:
            # Create a new appearance.
            appearanceLib: adsk.core.MaterialLibrary = _app.materialLibraries.itemById('BA5EE55E-9982-449B-9D66-9F036540E140')

            # Get the appearance using itemById as unlike itemByName it is not locale dependent.
            genericAppearance: adsk.core.Appearance = appearanceLib.appearances.itemById('Prism-129')

            # Clone the generic appearance.
            colorAppearance: adsk.core.Appearance = appearances.addByCopy(genericAppearance, modeName)

            # Get the 'Color' property using itemById as unlike itemByName it is not locale dependent.
            colorProperty: adsk.core.Property = colorAppearance.appearanceProperties.itemById('opaque_albedo')

            # Set the color of the appearance.
            colorProperty.value = modeColor[modeName]

        # Apply the appearance to the body.
        face.appearance = colorAppearance

    # Give control back to Fusion so it can update the graphics.
    adsk.doEvents()

def loadProjectFromURN(urn:str = None) -> adsk.core.Document:
    ''' Minimal self-contained function to load and return a document via URN or return None safely '''
    doc: adsk.core.Document = None
    app = adsk.core.Application.get()
    if urn is not None:
        try: # File not found causes an exception
            project: adsk.core.DataFile = app.data.findFileById(urn)
            if project:
                doc = app.documents.open(project, True)
            else:
                app.userInterface.messageBox(f'File not found for URN: {urn}!')
        except Exception as e:
            if str(e)[0:38] == '3 : Design is located in another team.':
                # Although the document has been loaded, variable 'doc' may not be populated
                if doc is None:
                    doc: adsk.core.Document = adsk.core.Application.get().activeDocument
            elif str(e)[0:20] == '3 : file not found':
                app.userInterface.messageBox(f'File not found for URN: {urn}!')
            else:
                # Abandon for unhandled errors, displaying the error message.
                app.userInterface.messageBox(f'Failed:{str(e)}\n{traceback.format_exc()}')
    return doc
```

