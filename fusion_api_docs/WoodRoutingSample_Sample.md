# Wood Routing Workflow Sample

## Description

This script demonstrates routing wood panels.

When running the sample, it assumes you have an open design containing one or more "panels" oriented flat in the X-Y plane. The script creates a setup and a 2D contour operation with tabs to route the panels from a standard sheet.

## Code Samples

| Copy Code |
|----------:|

```python
#Assumes a model is loaded in Fusion, eg a couple of flat panels 

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # use existing doc:
        doc = app.activeDocument

        # switch to manufacturing space
        camWS = ui.workspaces.itemById('CAMEnvironment') 
        camWS.activate()

        # get the CAM product
        products = doc.products

        #################### Search a tool in our tool library ####################
        # get the tool libraries from the library manager
        camManager = adsk.cam.CAMManager.get()
        libraryManager = camManager.libraryManager
        toolLibraries = libraryManager.toolLibraries

        # we can use a library URl directly if we know its address (using Fusion metric sample lib)
        url = adsk.core.URL.create('systemlibraryroot://Samples/Milling Tools (Metric).json')
        
        # load tool library
        toolLibrary = toolLibraries.toolLibraryAtURL(url)

        MyTool = None  
        # search an end mill for the contour operation
        for tool in toolLibrary:
            # read the tool type
            toolType = tool.parameters.itemByName('tool_type').value.value 
 
            # compare toolType and filter on 'flat end mill'
            if toolType == 'flat end mill' and not MyTool:
                # search for tool diameter larger or equal to 10mm but less than 12mm
                diameter = tool.parameters.itemByName('tool_diameter').value.value
                if diameter >= 1.0 and diameter < 1.2: 
                    MyTool = tool
                    break

        #################### create setup ####################
        cam = adsk.cam.CAM.cast(products.itemByProductType("CAMProductType"))
        setups = cam.setups
        setupInput = setups.createInput(adsk.cam.OperationTypes.MillingOperation)
        # create a list for the models to add to the setup Input
        models = [] 
          
        # loop across all bRep bodies and add them all to our model list
        countParts = cam.designRootOccurrence.bRepBodies.count
        i = 0
        while i < countParts:
            part = cam.designRootOccurrence.bRepBodies.item(i)
            models.append(part)
            i = i + 1
            
        # pass the model list to the setup input
        setupInput.models = models 
        # create the setup
        setup = setups.add(setupInput) 

        # change some properties of the setup & stock
        setup.name = 'CAM Woodworking Script Sample'  
        setup.stockMode = adsk.cam.SetupStockModes.FixedBoxStock
        # set setup origin in the corner
        setup.parameters.itemByName('wcs_origin_boxPoint').value.value = 'top 1'
        # set stock size XYZ
        setup.parameters.itemByName('job_stockFixedX').expression = '2440 mm'
        setup.parameters.itemByName('job_stockFixedY').expression = '1220 mm'
        setup.parameters.itemByName('job_stockFixedZ').expression = '18 mm'

        #################### 2D contour operation ####################
        # set operation properties
        input = setup.operations.createInput('contour2d')
        input.tool = MyTool
        input.displayName = '2D Contour'
        input.parameters.itemByName('tolerance').expression = '0.1 mm' 
        
        # add tabs
        # activate tabs group to enable tabs and be able to modify its parameters
        input.parameters.itemByName('group_tabs').expression = 'true'
        input.parameters.itemByName('tabWidth').expression = '18 mm'
        input.parameters.itemByName('tabHeight').expression = '18 mm'
        input.parameters.itemByName('tabDistance').expression = '100 mm'

        # add the operation to the setup
        contourOp = setup.operations.add(input)
        
        # add silhouette to contour selection for 2D contour operation
        # requires the operation to exist
        cadcontours2dParam: adsk.cam.CadContours2dParameterValue = contourOp.parameters.itemByName('contours').value
        chains = cadcontours2dParam.getCurveSelections()
        # calculate and add a new silhouette curve to the geometry selection list
        chains.createNewSilhouetteSelection()
        cadcontours2dParam.applyCurveSelections(chains)

        # calculate operation
        cam.generateToolpath(contourOp)

        #################### post process ####################
        # copy-paste from basic milling sample

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

