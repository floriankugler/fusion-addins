# PipeFeatures.add Method

Parent Object: [PipeFeatures](PipeFeatures.md)  

## Description

Creates a new Pipe feature.

## Syntax

"pipeFeatures_var" is a variable referencing a [PipeFeatures](PipeFeatures.md) object.

```python
returnValue = pipeFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [PipeFeature](PipeFeature.md) | Returns the newly created PipeFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [PipeFeatureInput](PipeFeatureInput.md) | A PipeFeatureInput object that defines the desired Pipe. Use the createInput method to create a new PipeFeatureInput object and then use methods on it (the PipeFeatureInput object) to define the Pipe. |

## Version

Introduced in version October 2023  

