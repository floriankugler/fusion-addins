#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

_app: adsk.core.Application = None
_ui: adsk.core.UserInterface = None
_embossCustFeatureDef: adsk.fusion.CustomFeatureDefinition = None
_custFeatureBeingEdited: adsk.fusion.CustomFeature = None
_handlers = []

def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui  = _app.userInterface

        # Create the command definition for the feature create.
        embossCreateCmdDef = _ui.commandDefinitions.addButtonDefinition('adskRoundEmbossCreate', 'Round Emboss', 'Creates round emboss for sheet metal punch operation.', 'Resources/RoundEmboss')

        # Add the create button the user interface.
        solidWS = _ui.workspaces.itemById('FusionSolidEnvironment')
        smCreatePanel = solidWS.toolbarPanels.itemById('SheetMetalCreatePanel')
        cntrl = smCreatePanel.controls.addCommand(embossCreateCmdDef, 'FusionSheetMetalFlangeCommand', False)
        cntrl.isPromoted = True
        cntrl.isPromotedByDefault = True

        # Connect the handler to the command created event for the emboss create.
        onCommandCreated = EmbossCreateCommandCreatedHandler()
        embossCreateCmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Create the command definition for the feature edit.
        embossEditCmdDef = _ui.commandDefinitions.addButtonDefinition('adskRoundEmbossEdit', 'Round Emboss Edit', 'Edits round emboss feature.', '')

        # Connect the handler to the command created event for the emboss edit.
        onCommandCreated = EmbossEditCommandCreatedHandler()
        embossEditCmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Create the emboss custom feature definition.
        global _embossCustFeatureDef
        _embossCustFeatureDef = adsk.fusion.CustomFeatureDefinition.create('adskRoundEmboss', 'Round Emboss', 'Resources/RoundEmboss')
        _embossCustFeatureDef.editCommandId = 'adskRoundEmbossEdit'
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Unload the add-in.
def stop(context):
    try:
        solidWS = _ui.workspaces.itemById('FusionSolidEnvironment')
        smCreatePanel = solidWS.toolbarPanels.itemById('SheetMetalCreatePanel')
        cmdCntrl = smCreatePanel.controls.itemById('adskRoundEmbossCreate')
        if cmdCntrl:
            cmdCntrl.deleteMe()

        embossCreateCmdDef = _ui.commandDefinitions.itemById('adskRoundEmbossCreate')
        if embossCreateCmdDef:
            embossCreateCmdDef.deleteMe()

        embossEditCmdDef = _ui.commandDefinitions.itemById('adskRoundEmbossEdit')
        if embossEditCmdDef:
            embossEditCmdDef.deleteMe()
    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the emboss creation command created event.
class EmbossCreateCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Add the inputs to the command dialog.
            pointSelInput = inputs.addSelectionInput('point', 'Point', 'Sketch point at center of emboss.')
            pointSelInput.addSelectionFilter('SketchPoints')
            pointSelInput.setSelectionLimits(1, 1)

            des: adsk.fusion.Design = _app.activeProduct
            inputs.addValueInput('diameter', 'Diameter', des.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(2.54))
            inputs.addValueInput('height', 'Height', des.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByReal(2.54 * 0.25))

            # Connect to the various command related events.
            onActivate = CreateActivateHandler()
            cmd.activate.add(onActivate)
            _handlers.append(onActivate)

            onPreSelect = PreSelectHandler()
            cmd.preSelect.add(onPreSelect)
            _handlers.append(onPreSelect)

            onExecutePreview = CreateExecutePreviewHandler()
            cmd.executePreview.add(onExecutePreview)
            _handlers.append(onExecutePreview)

            onExecute = CreateExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CreateActivateHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)

            # Code to react to the event.
            ShowMessage('In MyActivateHandler event handler.')
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class PreSelectHandler(adsk.core.SelectionEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.SelectionEventArgs.cast(args)

            # Only allow the selection of sketch points that have been
            # created on a sketch that was created on a face.
            skPoint: adsk.fusion.SketchPoint = eventArgs.selection.entity
            sk = skPoint.parentSketch
            if sk.referencePlane.objectType != adsk.fusion.BRepFace.classType():
                eventArgs.isSelectable = False
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CreateExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Get the inputs.
            pointSel: adsk.core.SelectionCommandInput = inputs.itemById('point')
            skPoint = pointSel.selection(0).entity
            diaInput: adsk.core.ValueCommandInput = inputs.itemById('diameter')
            heightInput: adsk.core.ValueCommandInput = inputs.itemById('height')

            # Create the emboss.
            CreateEmboss(skPoint, diaInput.expression, diaInput.value, heightInput.expression, heightInput.value)  

            # Code to react to the event.
            ShowMessage('In MyExecutePreviewHandler event handler.')
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CreateExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            ShowMessage('In MyExecuteHandler event handler.')
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Get the inputs.
            pointSel: adsk.core.SelectionCommandInput = inputs.itemById('point')
            skPoint: adsk.fusion.SketchPoint = pointSel.selection(0).entity
            diaInput: adsk.core.ValueCommandInput = inputs.itemById('diameter')
            heightInput: adsk.core.ValueCommandInput = inputs.itemById('height')

            # Create the emboss.
            (sk, fillet, diaParam, heightParam) = CreateEmboss(skPoint, diaInput.expression, diaInput.value, heightInput.expression, heightInput.value)

            # Create the custom feature.
            comp: adsk.fusion.Component = skPoint.parentSketch.parentComponent
            des = comp.parentDesign
            custFeatureInput = comp.features.customFeatures.createInput(_embossCustFeatureDef)
            custFeatureInput.addDependency('point', skPoint)
            custFeatureInput.addCustomParameter('diameter', 'Diameter', adsk.core.ValueInput.createByString(diaInput.expression), des.unitsManager.defaultLengthUnits, True)
            custFeatureInput.addCustomParameter('height', 'Height', adsk.core.ValueInput.createByString(heightInput.expression), des.unitsManager.defaultLengthUnits, True)
            custFeatureInput.setStartAndEndFeatures(sk, fillet)
            custFeature = comp.features.customFeatures.add(custFeatureInput)

            # Set the sketch and feature parameters to use the custom parameters.
            diaCustParam = custFeature.parameters.itemById('diameter')
            diaParam.expression = diaCustParam.name

            heightCustParam = custFeature.parameters.itemById('height')
            heightParam.expression = heightCustParam.name
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the custom feature compute event.
class EmbossComputeHandler(adsk.fusion.CustomFeatureEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.fusion.CustomFeatureEventArgs.cast(args)

            # Code to react to the event.
            ShowMessage('In EmbossComputeHandler event handler.')
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the emboss edit command created event.
class EmbossEditCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            ShowMessage('In EmbossEditCommandCreatedHandler event handler.')
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Get the custom feature being edited.
            global _custFeatureBeingEdited
            _custFeatureBeingEdited = _ui.activeSelections.item(0).entity

            # Get the values from the feature.
            diamParam = _custFeatureBeingEdited.parameters.itemById('diameter')
            heightParam = _custFeatureBeingEdited.parameters.itemById('height')

            # Add the inputs to the command dialog.
            des: adsk.fusion.Design = _app.activeProduct           
            inputs.addValueInput('diameter', 'Diameter', des.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByString(diamParam.expression))
            inputs.addValueInput('height', 'Height', des.unitsManager.defaultLengthUnits, adsk.core.ValueInput.createByString(heightParam.expression))

            # Connect to the required command related events.
            onExecutePreview = EditExecutePreviewHandler()
            cmd.executePreview.add(onExecutePreview)
            _handlers.append(onExecutePreview)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class EditExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            cmd = eventArgs.command
            inputs = cmd.commandInputs

            # Get the inputs.
            diaInput: adsk.core.ValueCommandInput = inputs.itemById('diameter')
            heightInput: adsk.core.ValueCommandInput = inputs.itemById('height')

            # Update the parameters.
            diamParam = _custFeatureBeingEdited.parameters.itemById('diameter')
            diamParam.expression = diaInput.expression
            heightParam = _custFeatureBeingEdited.parameters.itemById('height')
            heightParam.expression = heightInput.expression

            eventArgs.isValidResult = True
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def CreateEmboss(skPoint: adsk.fusion.SketchPoint, diaExp: str, diaVal: float, heightExp: str, heightVal: float):
    try:
        embossAngle = 30 * (math.pi / 180)

        # Get the face the sketch was created on.
        sk = skPoint.parentSketch
        face = sk.referencePlane
        if face.objectType != adsk.fusion.BRepFace.classType():
            return 'The selected point must be from a sketch on a face.'

        # Get the thickness of the part.
        thickness = GetThickness(face, skPoint.worldGeometry)
        if thickness == 0 or thickness > 0.25 * 2.54:
            return 'The thickness cannot be determined or the part is too thick.'

        comp: adsk.fusion.Component = face.body.parentComponent
        sk: adsk.fusion.Sketch = comp.sketches.addWithoutEdges(face)
        circles = sk.sketchCurves.sketchCircles
        
        # Copy the selected point into the new sketch.
        includedEnts = sk.include(skPoint)
        centerSkPoint: adsk.fusion.SketchPoint = includedEnts.item(0)

        # The dia is the size of the circle on the large side of the emboss.
        # The code below calculates the size of the smaller side so the wall
        # thickness maintains the material thickness.
        angle = (math.pi / 2 - embossAngle) / 2
        h = thickness / math.cos(angle)
        offset = h * math.sin(angle)
        skPstn = sk.modelToSketchSpace(centerSkPoint.geometry)
        outerCircle = circles.addByCenterRadius(skPstn, diaVal/2)
        innerCircle = circles.addByCenterRadius(skPstn, diaVal/2 - offset)

        # Add some constraints to contsrain the circles to the selected point
        # and the define the size.
        geomConst = sk.geometricConstraints
        geomConst.addCoincident(centerSkPoint, outerCircle.centerSketchPoint)
        geomConst.addConcentric(outerCircle, innerCircle)
        pstn = outerCircle.centerSketchPoint.geometry
        pstn.x += 0.5
        pstn.y += 0.5
        dimens = sk.sketchDimensions
        outerDim = dimens.addDiameterDimension(outerCircle, pstn)
        pstn = outerCircle.centerSketchPoint.geometry
        pstn.x -= 0.5
        pstn.y += 0.5
        innerDim = adsk.fusion.SketchDimension = dimens.addDiameterDimension(innerCircle, pstn)
        innerDim.parameter.expression = outerDim.parameter.name + ' - ' +  str(offset) + ' cm'
        diaParam = outerDim.parameter

        # Get the two profiles.
        prof: adsk.fusion.Profile
        for prof in sk.profiles:
            if prof.profileLoops.count == 1:
                innerProfile = prof
            elif prof.profileLoops.count == 2:
                outerProfile = prof

        # Create the extrusion for the outer part of the emboss.
        extrudes = comp.features.extrudeFeatures
        outerProfiles = adsk.core.ObjectCollection.create()
        outerProfiles.add(outerProfile)
        outerProfiles.add(innerProfile)
        extrudeInput = extrudes.createInput(outerProfiles, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(heightVal)), 
                                      adsk.fusion.ExtentDirections.PositiveExtentDirection, adsk.core.ValueInput.createByReal(-embossAngle))
        outerExtrude = extrudes.add(extrudeInput)

        # Get the name of the parameter that was created to control the height.
        distExtent: adsk.fusion.DistanceExtentDefinition = outerExtrude.extentOne
        heightParam = distExtent.distance
        heightParamName = heightParam.name

        # Create the extrude for the inner part of the emboss.
        extrudeInput = extrudes.createInput(innerProfile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString(heightParamName)), 
                                      adsk.fusion.ExtentDirections.PositiveExtentDirection, adsk.core.ValueInput.createByReal(-embossAngle))
        extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(-thickness))
        InnerExtrude = extrudes.add(extrudeInput)
        
        # Add the fillets.
        largeRad = heightVal
        smallRad = largeRad - thickness

        smallEdges = adsk.core.ObjectCollection.create()
        largeEdges = adsk.core.ObjectCollection.create()
        face: adsk.fusion.BRepFace
        for face in outerExtrude.faces:
            if face.geometry.objectType == adsk.core.Cone.classType():
                if face.edges.item(0).geometry.radius > face.edges.item(1).geometry.radius:
                    smallEdges.add(face.edges.item(0))
                    largeEdges.add(face.edges.item(1))
                else:
                    largeEdges.add(face.edges.item(0))
                    smallEdges.add(face.edges.item(1))

        for face in InnerExtrude.faces:
            if face.geometry.objectType == adsk.core.Cone.classType():
                if face.edges.item(0).geometry.radius > face.edges.item(1).geometry.radius:
                    largeEdges.add(face.edges.item(0))
                    smallEdges.add(face.edges.item(1))
                else:
                    smallEdges.add(face.edges.item(0))
                    largeEdges.add(face.edges.item(1))

        filletInput = comp.features.filletFeatures.createInput()
        filletInput.addConstantRadiusEdgeSet(smallEdges, adsk.core.ValueInput.createByReal(smallRad), False)
        filletInput.addConstantRadiusEdgeSet(largeEdges, adsk.core.ValueInput.createByReal(largeRad), False)
        fillet = comp.features.filletFeatures.add(filletInput)

        return (sk, fillet, diaParam, heightParam)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Give a face and a point on that face, determine the thickness of the part.
# This is intended to be used with sheet metal types of parts.
def GetThickness(face: adsk.fusion.BRepFace, pnt: adsk.core.Point3D):
    try:
        # Get the normal of the face, which will point outside the solid.
        eval = face.evaluator
        (_, ray) = eval.getNormalAtPoint(pnt)

        # Reverse the normal to point into the solid.
        ray.scaleBy(-1)

        comp = face.body.parentComponent
        foundEnts: adsk.core.ObjectCollection = None
        hitPoints = adsk.core.ObjectCollection.create()
        foundEnts = comp.findBRepUsingRay(pnt, ray, adsk.fusion.BRepEntityTypes.BRepFaceEntityType, -1, True, hitPoints)

        if foundEnts.item(0) == face:
            # The first hit returned is for the input face so use the second hit point.
            return pnt.distanceTo(hitPoints.item(1))
        else:
            return pnt.distanceTo(hitPoints.item(0))
    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def ShowMessage(message: str):
    textPalette: adsk.core.TextCommandPalette = _ui.palettes.itemById('TextCommands')
    if textPalette:
        textPalette.writeText(message)