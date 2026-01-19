# Rendering.startLocalRender Method

Parent Object: [Rendering](Rendering.md)  

## Description

Starts a local rendering process using either the active viewport or a specified camera to define the camera information. This starts a background process on the local machine to generate the rendering. Even though this is a background process, it is tied to the running Fusion process and will be terminated if Fusion is shut down. If multiple local renders are started, they are queued and only one runs at a time.

## Syntax

"rendering_var" is a variable referencing a [Rendering](Rendering.md) object.

```python
# Uses no optional arguments.
returnValue = rendering_var.startLocalRender()

# Uses optional arguments.
returnValue = rendering_var.startLocalRender(filename, camera)
```

## Return Value

| Type | Description |
|----|----|
| [RenderFuture](RenderFuture.md) | Returns a RenderFuture that allows you to check the current state of this rendering job. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filename | string | Optional argument that is the full path and filename of the file to write the resulting rendering to. The file extension can be .png, .jpg, .jpeg, or .tiff and the file will be saved as that type. If not provided or is an empty string, the rendering will be saved to the cloud as a PNG file. This is an optional argument whose default value is "". |
| camera | [Camera](Camera.md) | Optional argument that specifies the camera to use for the rendering. The default value is null, which will use the camera associated with the active viewport. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
| --- | --- |
| [Rendering Sample](RenderSample_Sample.md) | Demonstrates using the Rendering capabilities in the API. This starts a series of local renderings to generate a series of frames, where the camera is repositioned and a parameter is modified for each frame to create a dynamic animation. To use the sample, have a design open that contains a parameter named "Length". It can be a user or model parameter. The sample will modify this parameter from a value of 0.1 cm to 15 cm, but you can change these values by editing the values of the paramStartVal and paramEndVal variables on lines 90 and 91 of the sample. It expects a folder named "C:\Temp\RenderSample" to exist, and will fail if it doesn't. The rendered frames will be written to that folder. An example rendering is shown below where [this file](../ExtraFiles/RenderSample.f3d) was used. The parameter is modifying a move feature which results in changing the shape of an extrusion. The parameter could be driving anything and you could modify the code to edit more than one parameter. The result of this sample is a folder containing all of the rendered frames. You can process these to create an animation. The sample animation was created using GIMP. |

## Version

Introduced in version May 2023  

