# VolumetricSampler.evaluateColor Method

Parent Object: [VolumetricSampler](VolumetricSampler.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Evaluates the color of the model at the previously set sample points and returns the results.

## Syntax

"volumetricSampler_var" is a variable referencing a [VolumetricSampler](VolumetricSampler.md) object.

```python
returnValue = volumetricSampler_var.evaluateColor()
```

## Return Value

| Type | Description |
|----|----|
| [VolumetricColorSample](VolumetricColorSample.md)\[\] | An array of VolumetricColorSample objects that contain the results of sampling the volumetric model. |

## Version

Introduced in version May 2025  

