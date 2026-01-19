# Volumetric Custom Feature API Sample

## Description

Demonstrates how to create a Volumetric Custom Feature using the API for graph creation.

To run the sample script, have a document open in Fusion’s DESIGN workspace. This script will create a component with a box by sketching then extruding that sketch. It will then use that box as a boundary body and create a Volumetric Custom Feature.

The script will the create a gyroid lattice using the Volumetric Model API with the appropriate Graphs, Nodes and Connections for a minimal example. Finally, the script will convert that Volumetric Model to Mesh using the API and the VolumetricModelToMeshFeature.

## Code Samples

| Copy Code |
|----------:|

```python
# Description: This script is used to create a volumetric model in the API

import os, adsk.core, adsk.fusion, adsk.volume,  traceback, time


def CreateVolumetricModel(component:adsk.fusion.Component,body):
    """Creation of the volumetric model"""
    features = component.features
    
    #Creating volumetric model input with the body
    VolumetricCustomFeatures = features.volumetricCustomFeatures
    volumetricCustomFeatureInput = VolumetricCustomFeatures.createInput(body)
    volumetricCustomFeature = VolumetricCustomFeatures.add(volumetricCustomFeatureInput)

    # build a simple volume - returns type adsk.core.Base
    volumetricModel = volumetricCustomFeature.volumetricModel
    # cast to a adsk.volume.VolumetricModel
    volumetricModel = adsk.volume.VolumetricModel.cast(volumetricModel)

    return volumetricModel

def VolumetricGraph(volumetricModel):
    """Assigning graph and modifying it (adding volume/density)"""
    #AS LONG AS THE VOLUMETRIC MODEL IS NOT NULL, WE HAVE SUCCESSFULLY CREATED A VOLUMETRIC MODEL
    #Call the graph and create a volume using it. Add a simple sphere for density as offset.
    primaryGraph = volumetricModel.getGraph(adsk.volume.GraphTypes.PrimaryGraphType)
    cellGraph = volumetricModel.getGraph(adsk.volume.GraphTypes.CellGraphType)

    # All the channels are created by default as well as the Boundary sdf

    # Create a density node and connect it to the density channel (Primary Graph)
    node1 = primaryGraph.addNode("ConstantDensity", "ConstantScalar")
    node1.properties.itemByName("value").value = 0.5
    densityChannel = primaryGraph.getOutputNode(adsk.volume.GraphOutputNodeTypes.LatticeDensityOutputNodeType)
    assert primaryGraph.connect(node1, 0, densityChannel, 0), "Failed to connect the node to the density channel"
        
    # Create a coordinate node and connect it to the coordinate channel (Primary Graph)
    node2 = primaryGraph.addNode("NoTransform", "TransformCoords")
    node2.properties.itemByName("scaling").value = adsk.core.Vector3D.create(1, 2, 3) # Scale the lattice asymmetrically
    coordinateOutput = primaryGraph.getOutputNode(adsk.volume.GraphOutputNodeTypes.LatticeCoordinatesOutputNodeType)
    assert primaryGraph.connect(node2, 0, coordinateOutput, 0), "Failed to connect the node to the coordinate channel"
        
    # Get the density output node from the cell graph and connect the density node to it
    node3 = cellGraph.addNode("gyroid", "FunctionVectorToScalar")
    node3.properties.itemByName("function").value = "(sin(x*pi2)*cos(y*pi2)+sin(y*pi2)*cos(z*pi2)+sin(z*pi2)*cos(x*pi2))*0.333333333+0.5"
    cellDensityChannel = cellGraph.getOutputNode(adsk.volume.GraphOutputNodeTypes.CellLatticeShapeOutputNodeType)
    assert cellGraph.connect(node3, 0, cellDensityChannel, 0), "Failed to connect the node to the density channel"

def run(context):
    ui = None
    try:
    ### Lines from 56 to 84 preparing a document to work with. Creating a body and volumetric lattice.

        # ALL THIS CODE IS TO GET A BODY AND COMPONENT TO WORK WITH
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        # new component
        newCompOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        newComp = newCompOcc.component

        # create a new sketch
        sketches = newComp.sketches
        sketch = sketches.add(newComp.xYConstructionPlane)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(10, 10, 0))
        sketch.isComputeDeferred = False

        extrudeFeatures = newComp.features.extrudeFeatures
        extrudeInput = extrudeFeatures.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distanceExtent = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString('10 cm'))
        direction = adsk.fusion.ExtentDirections.PositiveExtentDirection
        extrudeInput.setOneSideExtent(distanceExtent, direction)
        extrude = extrudeFeatures.add(extrudeInput)

        body = extrude.bodies.item(0)
        body = body.createForAssemblyContext(newCompOcc)

    ### Creating a volumetric model
        comp = newCompOcc.component
        features = comp.features

        VolumetricCustomFeatures = features.volumetricCustomFeatures
        volumetricCustomFeatureInput = VolumetricCustomFeatures.createInput(body)
        volumetricCustomFeature = VolumetricCustomFeatures.add(volumetricCustomFeatureInput)

        # build a simple volume - returns type adsk.core.Base
        volumetricModel = volumetricCustomFeature.volumetricModel
        # cast to a adsk.volume.VolumetricModel for autocompletion
        volumetricModel = adsk.volume.VolumetricModel.cast(volumetricModel)

        VolumetricGraph(volumetricModel)

    ### Convert to volumetric feature to mesh.

        # Now we should have valid volumetric models We need to create a Volumetric Model To Mesh
        volumetricModelToMeshFeatures = features.volumetricModelToMeshFeatures
        volumetricModelToMeshFeatureInput = volumetricModelToMeshFeatures.createInput(volumetricModel)

        # Setting all the properties for the volumetric model to mesh feature, though defaults are fine.
        volumetricModelToMeshFeatureInput.isComputeSuspended  = True
        volumetricModelToMeshFeatureInput.isSmallShellsRemoved = True
        volumetricModelToMeshFeatureInput.isVolumetricModelRemoved = True
        volumetricModelToMeshFeatureInput.smallShellThreshold = adsk.core.ValueInput.createByString("0.05")
        volumetricModelToMeshFeatureInput.meshingApproach = adsk.fusion.VolumetricMeshingApproachTypes.VolumetricMeshingAdvancedType
        volumetricModelToMeshFeatureInput.refinementType  = adsk.fusion.VolumetricMeshRefinementTypes.VolumetricMeshRefinementMediumType

        # Create the volumetric model to mesh feature
        volumetricModelToMeshFeatures.add(volumetricModelToMeshFeatureInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

