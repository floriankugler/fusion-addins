# VolumetricSampler.setPlaneSampling Method

Parent Object: [VolumetricSampler](VolumetricSampler.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Calculates and sets the sample points to be used for sampling the volumetric model for a given resolution, plane and primary axis. The points will be distributed in a grid pattern on the plane, starting at the plane origin and extend in the primary axis and secodary axis for the axis size arguments. The secondary axis is calculated from the cross product of the plane normal and the primary axis. This will override any previously set sample points.

## Syntax

"volumetricSampler_var" is a variable referencing a [VolumetricSampler](VolumetricSampler.md) object.

```python
returnValue = volumetricSampler_var.setPlaneSampling(elementSize, plane, primaryAxis, primaryAxisSize, secondaryAxisSize)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | True if the sample points were set successfully. |

## Parameters

| Name | Type | Description |
|----|----|----|
| elementSize | double | The approximate spacing between sample points. The units used for the element size are centimeters. |
| plane | [Plane](Plane.md) | The plane on which the points will be distributed. |
| primaryAxis | [Vector3D](Vector3D.md) | The primary axis of the plane. This vector should be on the plane. The secondary axis of the plane is calculated as the cross-product of the plane normal and the primary axis |
| primaryAxisSize | double | The size of the plane in the primary axis direction. |
| secondaryAxisSize | double | The size of the plane in the secondary axis direction. |

## Version

Introduced in version May 2025  

