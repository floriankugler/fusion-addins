# Fillet Feature Edit API Sample

## Description

Demonstrates editing a fillet feature.  
To successfully run this sample you can use this [Code Samples](../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3Ch2%20class=)

| Copy Code |
|----------:|

```python
import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get active design, root component, and timeline.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent              
        timeline = design.timeline

        # Get the first fillet feature in the root component.
        fillet: adsk.fusion.FilletFeature = rootComp.features.filletFeatures[0]

        # Roll the timeline to just before the fillet.
        fillet.timelineObject.rollTo(True)

        # Iterate over the edge sets.
        edgeSet: adsk.fusion.FilletEdgeSet = None

        # Save the edges currently used by the edge sets into a list.
        edges = []
        for edgeSet in fillet.edgeSets:
            edges.append(edgeSet.edges[0])

        # Insert the last edge into the first index and remove the last edge.
        edges.insert(0, edges[len(edges)-1])
        edges.pop(len(edges)-1)

        # Process each edge set based on its type.
        for i in range(fillet.edgeSets.count):
            edgeSet = fillet.edgeSets[i]
            if edgeSet.objectType == adsk.fusion.ConstantRadiusFilletEdgeSet.classType():
                # Change the radious of the fillet.
                constantEdgeSet: adsk.fusion.ConstantRadiusFilletEdgeSet = edgeSet
                radiusParam = constantEdgeSet.radius
                radiusParam.value = radiusParam.value / 2.0

                # Toggle the continuity type between tangent and curvature.
                if constantEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType:
                    constantEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType
                elif constantEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType:
                    constantEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType

                # Change which edge is filleted.
                newEdge = adsk.core.ObjectCollection.create()
                newEdge.add(edges[i])
                constantEdgeSet.edges = newEdge
            elif edgeSet.objectType == adsk.fusion.VariableRadiusFilletEdgeSet.classType():
                variableEdgeSet: adsk.fusion.VariableRadiusFilletEdgeSet = edgeSet
                
                # Swap the values of the start and end radii.
                startRadiusParam = variableEdgeSet.startRadius
                endRadiusParam = variableEdgeSet.endRadius
                startVal = startRadiusParam.value
                startRadiusParam.expression = endRadiusParam.expression
                endRadiusParam.value = startVal

                # Edit the mid positions.
                midPositions = variableEdgeSet.midPositions  
                midRadii = variableEdgeSet.midRadii
                for j in range(0, midPositions.count):
                    # Change the position and radius of the mid positions.
                    pos = midPositions.item(j).value
                    pos = pos + ((1 - pos) * 0.25)
                    midPositions.item(j).value = pos

                    midRadii.item(j).value = midRadii.item(j).value * 1.5
                
                # Add a new position.                    
                newMidPosition = adsk.core.ValueInput.createByReal(0.25)
                newMidRadius = adsk.core.ValueInput.createByReal(startRadiusParam.value * 0.75)
                variableEdgeSet.addMidPosition(newMidPosition, newMidRadius)

                # Toggle the continuity type between tangent and curvature.
                if variableEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType:
                    variableEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType
                elif variableEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType:
                    variableEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType

                # Change which edge is filleted.
                newEdge = adsk.core.ObjectCollection.create()
                newEdge.add(edges[i])
                variableEdgeSet.edges = newEdge
            elif edgeSet.objectType == adsk.fusion.ChordLengthFilletEdgeSet.classType():
                chordLengthEdgeSet = adsk.fusion.ChordLengthFilletEdgeSet.cast(edgeSet)

                # Edit the chord length.
                chordLengthParam = chordLengthEdgeSet.chordLength
                chordLengthParam.value = chordLengthParam.value * .75

                # Edit the tangency weight.
                tangencyWeightParam = chordLengthEdgeSet.tangencyWeight
                tangencyWeightParam.value = tangencyWeightParam.value / 2                   

                # Toggle the continuity type between tangent and curvature.
                if chordLengthEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType:
                    chordLengthEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType
                elif chordLengthEdgeSet.continuity == adsk.fusion.SurfaceContinuityTypes.CurvatureSurfaceContinuityType:
                    chordLengthEdgeSet.continuity = adsk.fusion.SurfaceContinuityTypes.TangentSurfaceContinuityType

                # Change which edge is filleted.
                newEdge = adsk.core.ObjectCollection.create()
                newEdge.add(edges[i])
                chordLengthEdgeSet.edges = newEdge

        # Move the timeline back.
        timeline.moveToEnd()
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

