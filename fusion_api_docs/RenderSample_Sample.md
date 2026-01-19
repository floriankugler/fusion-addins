# Rendering Sample

## Description

Demonstrates using the Rendering capabilities in the API. This starts a series of local renderings to generate a series of frames, where the camera is repositioned and a parameter is modified for each frame to create a dynamic animation. To use the sample, have a design open that contains a parameter named "Length". It can be a user or model parameter. The sample will modify this parameter from a value of 0.1 cm to 15 cm, but you can change these values by editing the values of the paramStartVal and paramEndVal variables on lines 90 and 91 of the sample. It expects a folder named "C:\Temp\RenderSample" to exist, and will fail if it doesn't. The rendered frames will be written to that folder.

An example rendering is shown below where [this file](../ExtraFiles/RenderSample.f3d) was used. The parameter is modifying a move feature which results in changing the shape of an extrusion. The parameter could be driving anything and you could modify the code to edit more than one parameter. The result of this sample is a folder containing all of the rendered frames. You can process these to create an animation. The sample animation was created using GIMP.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core
import adsk.fusion
import traceback
import threading
import math

app = None
ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None
checkProgress = 'RenderProgress'
customEvent = None
renderFutures = []
checkCount = 0

app = adsk.core.Application.get()
ui  = app.userInterface
        
# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Display a seperator line, with a counter so it's easy to see it's processing.
            global checkCount
            checkCount += 1
            app.log(f'== {checkCount} ================================================')

            # Iterate through the render futures to display the status in the TEXT COMMAND window
            # and check to see if it's finished.
            stillProcessing = False
            future: adsk.fusion.RenderFuture
            for future in renderFutures:
                if future.renderState == adsk.fusion.LocalRenderStates.QueuedLocalRenderState:
                    app.log(f'Queued: {future.filename}')
                    stillProcessing = True
                elif future.renderState == adsk.fusion.LocalRenderStates.ProcessingLocalRenderState:
                    app.log(f'Processing: {future.filename}, Percent: {future.progress * 100}%')
                    stillProcessing = True

            if(not stillProcessing):
                # All jobs have been processed, so terminate the script. This will result
                # in the stop function being called where the final cleanup is done.
                app.log("Finished!")
                adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        # Every five seconds fire a custom event to check the rendering progress.
        while not self.stopped.wait(5):
            app.fireCustomEvent(checkProgress) 
        
        
def run(context):
    try:
        # Get the active Design
        des: adsk.fusion.Design = app.activeProduct

        # Get information from the current camera.
        cam = app.activeViewport.camera
        upVector = GetUpVector(cam)
        eye = cam.eye

        # Use the center of the bounding box as the target.
        boundBox = des.rootComponent.boundingBox
        target = adsk.core.Point3D.create((boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
                                          (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
                                          (boundBox.minPoint.z + boundBox.maxPoint.z) / 2)
        
        # Get the RenderManager from the Design and set the resolution of the output image.
        rm = des.renderManager
        render = rm.rendering
        render.resolution = adsk.fusion.RenderResolutions.Mobile960x640RenderResolution

        # Specify the number of frames to render.
        frames = 10

        # Define the parameter that will be modified and the start and end values.
        paramName = 'Length'
        paramStartVal = .1
        paramEndVal = 15
        param = des.allParameters.itemByName(paramName)

        # Create the rotation matrix that will be used for the eye point to rotate 
        # around the model.
        rotMatrix = adsk.core.Matrix3D.create()
        angle = (math.pi * 2) / frames
        rotMatrix.setToRotation(angle, upVector, target)

        # Start a rendering for each frame.
        for i in range(frames):
            # Set the camera for the current frame.
            cam.target = target
            cam.upVector = upVector
            cam.eye = eye

            # Set the parameter value for this frame.
            paramVal = ((paramEndVal - paramStartVal) / (frames - 1)) * i + paramStartVal
            param.value = paramVal
            #adsk.doEvents()

            # Define the filename for this frame.
            filename = f'C:/Temp/RenderSample/Frame{i:05d}.png'

            # Start the render.
            renderFutures.append(render.startLocalRender(filename, cam))
            app.log(f'Started frame {i}')
            app.log(f'   Parameter Value: {paramVal}')
            app.log(f'   Progress: {renderFutures[len(renderFutures)-1].progress}')
            app.log(f'   RenderState: {renderFutures[len(renderFutures)-1].renderState}')
            app.log(f'   imageWidth: {renderFutures[len(renderFutures)-1].imageWidth}')
            app.log(f'   imageHeight: {renderFutures[len(renderFutures)-1].imageHeight}')
            app.log(f'   fileName: {renderFutures[len(renderFutures)-1].filename}')

            # Transform the eye point for the next frame.
            eye.transformBy(rotMatrix)

        # Create a new thread that is used to watch the progress of the renders.
        # This is done in a seperate thread, so the Fusion main thread isn't blocked.
        global stopFlag        
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag)
        myThread.start()

        # Register the custom event and connect the handler.
        # This is done so the monitoring thread can trigger this
        # event to allow work to happen on Fusion's main thread.
        global customEvent
        customEvent = app.registerCustomEvent(checkProgress)
        onThreadEvent = ThreadEventHandler()
        customEvent.add(onThreadEvent)
        handlers.append(onThreadEvent)

        # Don't terminate the script, but allow it to keep running.
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        # Clean up the events.
        if handlers.count:
            customEvent.remove(handlers[0])
        stopFlag.set() 
        app.unregisterCustomEvent(checkProgress)

        ui.messageBox('Rendering is complete')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Given a camera, this determines in which of the primary axis
# directions, the up vector is closest to and return that vector.
def GetUpVector(camera: adsk.core.Camera) -> adsk.core.Vector3D:
    # Determine which of the primary directions the current up vector is closest to.
    upVector = adsk.core.Vector3D.create(1, 0, 0)
    angle = upVector.angleTo(camera.upVector)
    if adsk.core.Vector3D.create(-1, 0, 0).angleTo(camera.upVector) < angle:
        upVector = adsk.core.Vector3D.create(-1, 0, 0)
        angle = upVector.angleTo(camera.upVector)
    
    if adsk.core.Vector3D.create(0, 1, 0).angleTo(camera.upVector) < angle:
        upVector = adsk.core.Vector3D.create(0, 1, 0)
        angle = upVector.angleTo(camera.upVector)

    if adsk.core.Vector3D.create(0, -1, 0).angleTo(camera.upVector) < angle:
        upVector = adsk.core.Vector3D.create(0, -1, 0)
        angle = upVector.angleTo(camera.upVector)

    if adsk.core.Vector3D.create(0, 0, 1).angleTo(camera.upVector) < angle:
        upVector = adsk.core.Vector3D.create(0, 0, 1)
        angle = upVector.angleTo(camera.upVector)

    if adsk.core.Vector3D.create(0, 0, -1).angleTo(camera.upVector) < angle:
        upVector = adsk.core.Vector3D.create(0, 0, -1)
        angle = upVector.angleTo(camera.upVector)

    return upVector
```

