# PipeFeatures.createInput Method

Parent Object: [PipeFeatures](PipeFeatures.md)  

## Description

Creates a PipeFeatureInput object for defining a simple Pipe feature with only a path. Use properties and methods on this object to define the Pipe you want to create and then use the Add method, passing in the PipeFeatureInput object.

## Syntax

"pipeFeatures_var" is a variable referencing a [PipeFeatures](PipeFeatures.md) object.

```python
returnValue = pipeFeatures_var.createInput(path, operation)
```

## Return Value

| Type | Description |
|----|----|
| [PipeFeatureInput](PipeFeatureInput.md) | Returns the newly created PipeFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| path | [Path](Path.md) | The path to create the Pipe. |
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform. |

## Version

Introduced in version October 2023  

