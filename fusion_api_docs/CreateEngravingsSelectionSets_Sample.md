# Create Engravings Selection Sets API Sample

## Description

This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition.

The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions.

We assume here that an engraving pocket is:

- Made with a flat bottom face and no fillet.
- A closed pocket.
- Have a Z height less than 2 mm

We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation.

The engraving toolpath can be seen by expanding the setup and selecting the operation.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback

PROJECT_URN = 'urn:adsk.wipprod:fs.file:vf.XhO3KCCLTUi83YJLaAiCRg?version=1'
TOOL_LIBRARY_URN = 'systemlibraryroot://Samples/Milling Tools (Metric).json'

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Open document by its URN.
        doc = loadProjectFromURN(PROJECT_URN)
        if doc is None:
            return

        # Switch to the manufacturing space.
        camWS = ui.workspaces.itemById('CAMEnvironment')
        camWS.activate()

        # Get the cam product.
        products = doc.products
        cam: adsk.cam.CAM = products.itemByProductType('CAMProductType')

        # Get the design product.
        design: adsk.fusion.Design = products.itemByProductType('DesignProductType')

        ############# Find design and manufacturins bRepBodies #############

        # Get the first body of the design root component.
        designBody = design.rootComponent.bRepBodies.item(0)

        # Find the equivalent body in manufacturing space.
        comp = designBody.parentComponent
        camBody: adsk.fusion.BRepBody = None
        for body in cam.designRootOccurrence.bRepBodies:
            if body.parentComponent.name == comp.name:
                camBody = body
                break

        ############# Find engravings using pocket recognition #############

        # Define recognition vector: recognize pockets on top side (Z- view direction).
        searchVector = adsk.core.Vector3D.create(0, 0, -1)

        # Recognize any pockets in the design body.
        recognizedPockets = adsk.cam.RecognizedPocket.recognizePockets(designBody, searchVector)

        # Identify pockets that may be engravings based on their dimensions.
        # We assume here that an engraving pocket is:
        #  - made of a flat bottom face (no fillet or such)
        #  - must be a closed pocket
        #  - Z height is less than 2 mm
        POCKET_MAX_DEPTH = 0.2

        engravingFeatures: list[EngravingFeature] = []
        for recognizedPocket in recognizedPockets:
            # Pocket must be closed.
            if recognizedPocket.isClosed:
                # Check the pocket depth.
                if recognizedPocket.depth  adsk.core.Document:
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

