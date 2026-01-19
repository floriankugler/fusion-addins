# Basic Milling Workflow Sample

## Description

Demonstrates the creation of a basic milling workflow from script

Demonstrates creating a setup, searching tool library to retrieve a tool, create a couple of machining operations and a NC program, ready for post processing.

Use the 2D Strategies model from the Fusion CAM Samples folder as your CAD model.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, adsk.cam, traceback
import time

def run(context):
    ui = None
    try:

        #################### Initialisation #####################
        app = adsk.core.Application.get()
        ui  = app.userInterface

        PROJECT_URN = 'urn:adsk.wipprod:fs.file:vf.KoBHzV4mTOiNvFStiBwpzA?version=1' # Production

        # Load by URN a specific sample project to demonstrate a basic milling workflow.
        doc = loadProjectFromURN(PROJECT_URN)
        if doc is None: 
            return

        # Switch to manufacturing space
        camWS: adsk.core.Workspace = ui.workspaces.itemById('CAMEnvironment')
        camWS.activate()

        # Get the CAM product
        products: adsk.core.Products = doc.products

        #################### Find tools in sample tool library ####################
        # Get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager: adsk.cam.CAMLibraryManager = camManager.libraryManager
        toolLibraries: adsk.cam.ToolLibraries = libraryManager.toolLibraries

        # We can use a library URl directly if we know its address (here we use Fusion's Metric sample library)
        url = adsk.core.URL.create('systemlibraryroot://Samples/Milling Tools (Metric).json')

        # Load tool library
        toolLibrary: adsk.cam.ToolLibrary = toolLibraries.toolLibraryAtURL(url)

        # Create some variables for the milling tools which will be used in the operations
        faceTool: adsk.cam.Tool = None
        adaptiveTool: adsk.cam.Tool = None

        # Searching the face mill and the bull nose using a loop for the roughing operations
        for tool in toolLibrary:
            # Read the tool type
            toolType = tool.parameters.itemByName('tool_type').value.value

            # Select the first face tool found
            if toolType == 'face mill' and not faceTool:
                faceTool = tool

            # Search the roughing tool
            elif toolType == 'bull nose end mill' and not adaptiveTool:
                # We look for a bull nose end mill tool larger or equal to 10mm but less than 14mm
                diameter = tool.parameters.itemByName('tool_diameter').value.value
                if diameter >= 1.0 and diameter  adsk.core.Document:
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

