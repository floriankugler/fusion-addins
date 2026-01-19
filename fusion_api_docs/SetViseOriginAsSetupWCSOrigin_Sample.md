# Set Vise Origin As Setup WCS Origin API Sample

## Description

This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin.

The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods:

Setup by default with no origin defined.

Setup using vise origin as WCS origin.

Setup using a sketch point as WCS origin.

Setup using a joint origin as WCS origin.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback

# Project URN for this script to open.
PROJECT_URN = 'urn:adsk.wipprod:fs.file:vf.Bp9h61ZBSzyiNd47VexneA?version=1'

# Name of project components, sketch and joint origin.
MODEL_COMPONENT_NAME = 'Model'
STOCK_COMPONENT_NAME = 'Stock'
VISE_COMPONENT_NAME = 'Vise'
VISE_COMPONENT_SKETCH_NAME = 'Sketch with a SkethPoint representing origin location'
VISE_COMPONENT_JOINT_ORIGIN_NAME = 'Vise Joint Origin'

# Name of the setup that will be created.
SETUP_NO_ORIGIN = 'Setup by default (no origin defined)'
SETUP_BY_ORIGIN = 'Setup using vise origin as WCS origin'
SETUP_BY_SKETCH = 'Setup using sketch point as WCS origin'
SETUP_BY_JOINT_ORIGIN = 'Setup using joint origin as WCS origin'


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Open document by its URN
        doc = loadProjectFromURN(PROJECT_URN)
        if doc is None:
            return

        # Switch to the manufacturing workspace.
        camWS = ui.workspaces.itemById('CAMEnvironment')
        camWS.activate()

        # Get the cam product.
        products = doc.products
        cam: adsk.cam.CAM = products.itemByProductType('CAMProductType')

        # Get design product.
        design: adsk.fusion.Design = products.itemByProductType('DesignProductType')
       
        # Find the occurences of the components that we need to pass to the setups.
        occurrences = design.rootComponent.allOccurrences
        models: list[adsk.fusion.Occurrence] = []
        stocks: list[adsk.fusion.Occurrence] = []
        fixtures: list[adsk.fusion.Occurrence] = []
        fixtureOrigin: adsk.fusion.ConstructionPoint = None

        for occurrence in occurrences:
            if occurrence.component.name == VISE_COMPONENT_NAME:
                fixtures.append(occurrence)
                # Get the construction point in its assembly context to return 
                # the originConstructionPoint equivalent in the cam workspace.
                fixtureOrigin = occurrence.component.originConstructionPoint.createForAssemblyContext(occurrence)
            elif occurrence.component.name == STOCK_COMPONENT_NAME:
                stocks.append(occurrence)
            elif occurrence.component.name == MODEL_COMPONENT_NAME:
                models.append(occurrence)

        ####### Create a first setup with no origin assignment. We can compare the difference over the rest.#######             
        setupBasic = createBaseSetup(cam, models, stocks, fixtures, SETUP_NO_ORIGIN)

        ####### Create a second setup and assign the vise origin point as setup origin. #######
        # Create a base setup...
        setupVise = createBaseSetup(cam, models, stocks, fixtures, SETUP_BY_ORIGIN)
        # ... then modify its origin.
        setupVise.parameters.itemByName('wcs_orientation_mode').expression = "'coordinateSystem'"
        setupVise.parameters.itemByName('wcs_orientation_cSys').value.value = [fixtureOrigin]

        ####### create a third setup and assign the sketch point as setup origin... #######
        # Get the sketch that contains the point we want to use.
        firstFixtureComponent = fixtures[0].component
        sketch = firstFixtureComponent.sketches.itemByName(VISE_COMPONENT_SKETCH_NAME)

        # The first sketchPoint item(0) is the sketch origin, we're interested in the second point here:
        # the one we manually added to the sketch to define an origin point item(1).
        sketchPoint = sketch.sketchPoints.item(1)

        # Create a base setup...
        setupSketch = createBaseSetup(cam, models, stocks, fixtures, SETUP_BY_SKETCH)
        # ... then modify its origin.
        setupSketch.parameters.itemByName('wcs_orientation_mode').expression = "'modelOrientation'"
        setupSketch.parameters.itemByName('wcs_origin_mode').expression = "'point'"
        setupSketch.parameters.itemByName('wcs_origin_point').value.value = [sketchPoint]

        ####### Create a fourth setup and assign the joint origin point as setup origin. #######
        # Get the joint origin we want to use
        jointOrigin = fixtures[0].component.jointOrigins.itemByName(VISE_COMPONENT_JOINT_ORIGIN_NAME)

        # Create a base setup...
        setupSketch = createBaseSetup(cam, models, stocks, fixtures, SETUP_BY_JOINT_ORIGIN)
        # ... then modify its origin.
        setupSketch.parameters.itemByName('wcs_orientation_mode').expression = "'modelOrientation'"
        setupSketch.parameters.itemByName('wcs_origin_mode').expression = "'point'"
        setupSketch.parameters.itemByName('wcs_origin_point').value.value = [jointOrigin]

        # Raise a done! message.
        setupMsg = f'\n- {SETUP_NO_ORIGIN}\n- {SETUP_BY_ORIGIN}\n- {SETUP_BY_SKETCH}\n- {SETUP_BY_JOINT_ORIGIN}'
        ui.messageBox(f'Setups created: \n{setupMsg}',
                        'Fusion\t\t\t',
                        adsk.core.MessageBoxButtonTypes.OKButtonType,
                        adsk.core.MessageBoxIconTypes.InformationIconType)

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:{e}\n{traceback.format_exc()}',
                            'Fusion\t\t\t',
                            adsk.core.MessageBoxButtonTypes.OKButtonType,
                            adsk.core.MessageBoxIconTypes.CriticalIconType)


def createBaseSetup(cam: adsk.cam.CAM, models: list[adsk.fusion.Occurrence], \
                    stocks: list[adsk.fusion.Occurrence], fixtures: list[adsk.fusion.Occurrence], name: str):
    ''' Create a basic setup with no origin defined'''
    # Create setup input object.
    setupInput = cam.setups.createInput(adsk.cam.OperationTypes.MillingOperation)
    setupInput.name = name

    # Set model.
    setupInput.models = models

    # Set fixture.
    setupInput.fixtureEnabled = True
    setupInput.fixtures = fixtures

    # Create the setup.
    setup = cam.setups.add(setupInput)

    # Set stock on the setup. After the first setup is created, the newly created setups are created with
    # default stock equivalent to their preceeding stock so, applying this to the setup to overwrite default
    objCollection = adsk.core.ObjectCollection.createWithArray(stocks)
    setup.stockMode = adsk.cam.SetupStockModes.SolidStock
    setup.stockSolids = objCollection

    # Return created setup
    return setup

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

