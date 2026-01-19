# Matrix3D.setToRotation Method

Parent Object: [Matrix3D](Matrix3D.md)  

## Description

Sets this matrix to the matrix of rotation by the specified angle, through the specified origin, around the specified axis

## Syntax

"matrix3D_var" is a variable referencing a [Matrix3D](Matrix3D.md) object.

```python
returnValue = matrix3D_var.setToRotation(angle, axis, origin)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name   | Type                     | Description                               |
|--------|--------------------------|-------------------------------------------|
| angle  | double                   | The rotation angle in radians.            |
| axis   | [Vector3D](Vector3D.md) | The axis of rotation.                     |
| origin | [Point3D](Point3D.md)   | The origin point of the axis of rotation. |

## Samples

| Name | Description |
| --- | --- |
| [Rendering Sample](RenderSample_Sample.md) | Demonstrates using the Rendering capabilities in the API. This starts a series of local renderings to generate a series of frames, where the camera is repositioned and a parameter is modified for each frame to create a dynamic animation. To use the sample, have a design open that contains a parameter named "Length". It can be a user or model parameter. The sample will modify this parameter from a value of 0.1 cm to 15 cm, but you can change these values by editing the values of the paramStartVal and paramEndVal variables on lines 90 and 91 of the sample. It expects a folder named "C:\Temp\RenderSample" to exist, and will fail if it doesn't. The rendered frames will be written to that folder. An example rendering is shown below where [this file](../ExtraFiles/RenderSample.f3d) was used. The parameter is modifying a move feature which results in changing the shape of an extrusion. The parameter could be driving anything and you could modify the code to edit more than one parameter. The result of this sample is a folder containing all of the rendered frames. You can process these to create an animation. The sample animation was created using GIMP. |

## Version

Introduced in version August 2014  

