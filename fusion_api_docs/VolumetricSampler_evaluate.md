# VolumetricSampler.evaluate Method

Parent Object: [VolumetricSampler](VolumetricSampler.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Evaluates the volumetric model at the previously set sample points for the given node and returns the results.

## Syntax

"volumetricSampler_var" is a variable referencing a [VolumetricSampler](VolumetricSampler.md) object.

```python
# Uses no optional arguments.
returnValue = volumetricSampler_var.evaluate(graphNode)

# Uses optional arguments.
returnValue = volumetricSampler_var.evaluate(graphNode, isOutput, index)
```

## Return Value

| Type | Description |
|----|----|
| [VolumetricSample](VolumetricSample.md)\[\] | An array of VolumetricSample objects that contain the results of sampling the volumetric model. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| graphNode | [GraphNode](GraphNode.md) | The graph node to evaluate at the sample points. |
| isOutput | boolean | Optional argument that controls the sampling. If set to true samples an output pin, if set to false samples an input pin. Default is True. This is an optional argument whose default value is True. |
| index | integer | Optional argument that controls the index of the pin to sample. Default is 0 which is the first pin. This is an optional argument whose default value is 0. |

## Version

Introduced in version May 2025  

